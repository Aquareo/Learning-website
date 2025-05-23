## GPT4o给我提了一个问题：ApplicationContext是如何创建Bean的？

> Bean 是 Spring 中的 Object，也可以理解为 Object + Spring 的管理机制。

我写了一个用于查看 Spring 源码流程的测试代码，下面是完整的代码：

```java
package com.origin;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.stereotype.Component;

@Component
class SimpleBean {

    public SimpleBean() {
        System.out.println("1. SimpleBean 构造函数被调用");
    }

    @PostConstruct
    public void init() {
        System.out.println("2. SimpleBean 初始化方法被调用");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("3. SimpleBean 销毁方法被调用");
    }
}

public class Main {
    public static void main(String[] args) {
        AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");

        // 反射构造
        SimpleBean bean = context.getBean(SimpleBean.class);

        context.close();
    }
}
```

这里的注解 `@Component` 是告诉 Spring：“Spring 快看过来，我这个类 `SimpleBean` 是一个 Bean 哦！”

```java
@Component
class SimpleBean {}
```

我们在这个 Bean 里面实现了构造函数、初始化方法 `init()`、销毁方法 `destroy()`，来观察 Spring 在创建和销毁 Bean 时的顺序。

---

## 看一下 `main` 函数的三句话：

```java
public class Main {
    public static void main(String[] args) {

        AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");

        // 反射构造
        SimpleBean bean = context.getBean(SimpleBean.class);

        context.close();
    }
}
```

这三句话的意思分别是：

1. 创建一个容器，名为 `context`（Spring 用来管理 Bean 的“工厂”叫做容器）；
2. 使用反射构造一个 `SimpleBean` 的对象（反射是 Java 里一种很抽象但有用的机制，简单来说就是“不走寻常路”来创建对象）；
3. 关闭刚才创建的容器。

---

## 运行结果：

```
1. SimpleBean 构造函数被调用  
2. SimpleBean 初始化方法被调用  
3. SimpleBean 销毁方法被调用
```

---

## ApplicationContext 创建 Bean 的过程（源码调试）

我通过设置断点，调试了一下午终于搞懂了这三句话的底层逻辑。下面详细解读每一步：

### 1. 初始化容器

```java
AnnotationConfigApplicationContext context = 
    new AnnotationConfigApplicationContext("com.origin");
```

这句话是初始化容器。Spring 容器通过扫描指定的包 `com.origin`（也就是我们用 `@Component` 标注的类所在包）来找出有哪些类应该注册成 Bean。

当然，也可以通过配置文件来搞，比如 XML 配置：

```xml
<bean id="SimpleBean" class="com.origin.SimpleBean"/>
```

这和 `@Component` 的作用类似，都是声明 Bean，只不过形式不同。这个过程叫做 **注册 Bean**。

---

### 2. 创建 Bean 实例

关键在这句话：

```java
SimpleBean bean = context.getBean(SimpleBean.class);
```

调用链如下：

```
AbstractApplicationContext.getBean()
├── getBeanFactory().getBean()
│   ├── doGetBean()
│   │   ├── 检查单例缓存
│   │   ├── 创建 Bean（如果不存在）
│   │   │   ├── createBean()
│   │   │   │   ├── 解析 Bean 类
│   │   │   │   ├── 前置处理
│   │   │   │   ├── doCreateBean()
│   │   │   │   │   ├── createBeanInstance() // 实例化
│   │   │   │   │   │   └── 使用反射调用构造函数
│   │   │   │   │   ├── populateBean()      // 属性填充
│   │   │   │   │   └── initializeBean()    // 初始化
│   │   │   │   │       ├── invokeAwareMethods()
│   │   │   │   │       ├── applyBeanPostProcessorsBeforeInitialization()
│   │   │   │   │       │   └── @PostConstruct
│   │   │   │   │       └── applyBeanPostProcessorsAfterInitialization()
│   │   │   │   └── 后置处理
│   │   │   └── 加入单例缓存
│   │   └── 返回 Bean 实例
│   └── 类型转换（如果需要）
└── 返回 Bean
```

这个图其实可以不用死记硬背，简单来说就是：

* `getBean()` 先检查缓存有没有这个 Bean；
* 没有就调用 `doGetBean()` 创建 Bean；
* 然后往下一直调用，最终使用 Java 反射来实例化这个类。

---

### Java 反射创建实例的关键方法：

```java
public T newInstance(Object... initargs) {
    Class<?> caller = override ? null : Reflection.getCallerClass();
    return newInstanceWithCaller(initargs, !override, caller);
}
```

这里：

* `initargs`：就是构造函数的参数，Spring 会根据需要填充；
* `Reflection.getCallerClass()`：拿到调用者信息，主要用于安全校验；
* 最终调用 `constructorToUse.newInstance(args)` 来创建实例。

---

### 2.1 Spring 是如何选择构造器的？

Spring 使用 `InstantiationStrategy`（默认是 `SimpleInstantiationStrategy`）来选择构造器：

```java
constructorToUse.setAccessible(true);
return (T) constructorToUse.newInstance(args);
```

如果使用的是无参构造器：

```java
constructorToUse.newInstance(); // 等价于 newInstance(new Object[0])
```

如果有参数，那 Spring 会自动解析依赖，准备参数：

```java
constructorToUse.newInstance(args);
```

---

### 依赖注入

Spring 会解析 `@Autowired` 或构造函数的参数，决定是否注入其他依赖：

```java
class A {
    @Autowired
    private B b;
}
```

实例化 A 时，Spring 会先创建并注入 B。

---

### 调用 `init()` 方法

这个一般是做一些初始化或准备工作，Spring 会自动调用。

---

### 放入容器缓存

创建完后，Spring 会将其加入单例池中，便于后续复用。

---

## Bean 的依赖注入顺序：两个例子

### 第一个例子：

测试代码如下：

```java
@Component
class SimpleBean {
    @Autowired
    private DependentBean dependentBean;
    ...
}

@Component
class DependentBean {
    ...
}
```

输出：

```
1. DependentBean 构造函数被调用  
2. DependentBean 初始化方法被调用  
1. SimpleBean 构造函数被调用  
2. SimpleBean 初始化方法被调用  
3. SimpleBean 销毁方法被调用  
3. DependentBean 销毁方法被调用
```

结论：

> Spring 会先创建依赖 Bean（`DependentBean`），再创建主 Bean（`SimpleBean`）。销毁顺序则相反。

---

### 第二个例子：

仅仅把类名替换成 A 和 B，结构不变：

```java
@Component
class A {
    @Autowired
    private B b;
    ...
}

@Component
class B {
    ...
}
```

输出变为：

```
1. A 构造函数被调用  
1. B 构造函数被调用  
2. B 初始化方法被调用  
2. A 初始化方法被调用  
3. A 销毁方法被调用  
3. B 销毁方法被调用
```

这是为什么？！

---

## 真相：**Bean 的注册顺序决定了谁先触发构造！**

调用：

```java
new AnnotationConfigApplicationContext("com.origin");
```

Spring 会扫描 `com.origin` 包，并按 **类名字典序** 注册 Bean。

举例：

* 如果注册顺序是 `[A, B]`，那 A 会先被创建；
* A 被创建时发现依赖 B，就顺手创建 B。

这就导致了输出顺序变了。

---

## 如何验证这个说法？

加入一个自定义的 `BeanFactoryPostProcessor` 打印注册顺序：

```java
@Component
class MyBeanFactoryPostProcessor implements BeanFactoryPostProcessor {
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory factory) {
        System.out.println("Spring 注册的 Bean 顺序：");
        for (String name : factory.getBeanDefinitionNames()) {
            System.out.println("  -> " + name);
        }
    }
}
```

验证结果：

* 第一个例子注册顺序为：

  ```
  -> dependentBean
  -> myBeanFactoryPostProcessor
  -> simpleBean
  ```

* 第二个例子注册顺序为：

  ```
  -> a
  -> b
  -> myBeanFactoryPostProcessor
  ```

这验证了我们前面的结论。

---

## 新问题：**为什么只是简单的类名替换，注册顺序就变了？**

### 猜想：**Spring 注册 Bean 的时候是按名字进行字典序排序的！**

验证方法：写一堆不同名字的类，并且打乱顺序：

```java
@Component class Beta {}
@Component class Charlie {}
@Component class Alpha {}
@Component class Delta {}
@Component class Echo {}
@Component class Edho {}
@Component class Foxtrot {}
```

输出注册顺序：

```
-> alpha  
-> beta  
-> charlie  
-> delta  
-> echo  
-> edho  
-> foxtrot  
-> myBeanFactoryPostProcessor
```

**完全符合字典序！**

---

## Spring 源码中哪里体现了字典序？

调用链：

```java
new AnnotationConfigApplicationContext("com.example");
```

Spring 实际用的是 `ClassPathScanningCandidateComponentProvider` 来加载类。而加载类时：

* 用到 Java 的 `File.listFiles()` 或 `JarFile.entries()`；
* 这些方法返回的就是**按文件系统顺序（通常近似字典序）**；
* 所以注册顺序不是 Spring 显式排序，而是受底层文件系统影响。

---

## 最后一个点：**为什么销毁顺序和构造顺序相反？**

举个例子：

```java
@Component
class ConnectionManager {
    public void close() {
        System.out.println("关闭数据库连接");
    }
}

@Component
class UserService {
    @Autowired
    ConnectionManager connectionManager;

    @PreDestroy
    public void shutdown() {
        System.out.println("UserService 做一些资源释放");
    }
}
```

如果先销毁 `ConnectionManager`，`UserService` 的销毁逻辑可能就无法正常执行（比如记录日志）。所以 Spring 必须保证：

> **先销毁使用别人的那一方，再销毁被依赖的一方。**

这就是“后进先出”的管理原则。



---

### ✅ Spring Bean 生命周期与注册顺序：完整总结

1. **创建容器时，Spring 会扫描指定包下的类（如 `"com.origin"`）并注册为 Bean。**

   * 注册顺序**通常是按类名的字典序**，由 `ClassPathScanningCandidateComponentProvider` 处理；
   * 实际行为也受到类加载器、文件系统、构建工具等因素影响，**不建议依赖它做关键逻辑**。

2. **Spring 创建 Bean 的完整流程包括：**

   * 实例化（通过反射构造函数）；
   * 属性注入（字段或构造注入）；
   * 初始化（执行 `@PostConstruct` 或 `InitializingBean`）；
   * 缓存单例（加入容器）；
   * 销毁（容器关闭时执行 `@PreDestroy` 或 `DisposableBean`）。

3. **构造顺序受“注册顺序 + 依赖”双重影响：**

   * 如果主 Bean 比依赖先注册，就会先构造主 Bean，再顺带创建它的依赖；
   * 如果依赖先注册，自然就会先构造依赖，再构造主 Bean；
   * 所以**构造顺序≠依赖顺序**，尤其在使用字段注入时。

4. **销毁顺序严格反向于创建顺序：**

   * Spring 采用“后进先出”策略（LIFO），确保先销毁使用别人的 Bean；
   * 这是为了解决依赖在销毁阶段可能还要被用到的问题（比如日志、连接池等）。

5. **验证注册顺序的实用技巧：**

   * 实现 `BeanFactoryPostProcessor`，在 `postProcessBeanFactory()` 中打印 `beanDefinitionNames`；
   * 可以看到 Spring 实际注册的顺序，有助于分析构造时序。

6. **推荐：尽量使用构造注入，避免依赖注册顺序引发的混淆。**

   * 构造注入明确表达依赖关系，有利于测试和重构；
   * 字段注入虽然简单，但行为更依赖 Spring 的“内部处理机制”。

---

### 🔚 总结一句话：

> Spring 创建 Bean 的顺序虽然看似自动，但实则受多种因素影响：**注册顺序、依赖关系、注入方式**。理解这些内部机制，有助于我们在调试、排查 Bean 初始化异常时做到心中有数。

---

这段总结可以直接贴在文章末尾，作为“全景复盘”。如果你想要我帮你写个标题或配图文风格的结尾也可以说一声，我可以风格化一下。你希望是更口语化的？还是偏正式、适合发到公众号或技术博客的？
