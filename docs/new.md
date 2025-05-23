GPT4o给我提了一个问题：ApplicationContext是如何创建Bean的？

Bean是Spring中的Object。 Bean可以看做Object+Spring的管理机制


我写了一个查看Spring源码的代码的测试代码

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
        
        //反射构造
        SimpleBean bean = context.getBean(SimpleBean.class);

        context.close();
    }
}

```

这里的注释`@Component`是告诉Spring，Spring快看过来，我这个类SimpleBean是一个Bean噢！

```java
@Component
class SimpleBean {
}
```

实现三个Bean内部的重要方法，来观察其顺序，构造`SimpleBean()`，初始化`init()`，销毁`destroy()`.




再看`main`函数里面的三句话

```java
public class Main {
    public static void main(String[] args) {

        AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");
        
        //反射构造
        SimpleBean bean = context.getBean(SimpleBean.class);

        context.close();
    }
}

```

这三句话的意思分别是：
- 1.创建一个容器，名为`context`（Spring用来管理Bean的"工厂"叫做容器）
- 2.反射构造一个SimpleBean的对象（反射是java里面抽象又有用的特性，简单来说就是不走寻常路，创建一个对象）
- 3.关闭刚才创建的容器


不出意外运行结果为
```
1. SimpleBean 构造函数被调用
2. SimpleBean 初始化方法被调用
3. SimpleBean 销毁方法被调用
```


## ApplicationContext创建Bean

通过设置断点，调试了一下午终于搞懂，这三句话的底层逻辑

下面详细解读下这三句话

### 1.初始化容器

```java
 AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");
```

这句话是初始化容器，Spring容器通过扫描指定包`com.origin`
（我们之前指定的`@Component`）


当然还有另一种方式，用配置文件来搞，比如XML配置文件定义，就可以知道有哪些Bean需要管理

```XML
//这句话和@Component的作用类似，声明Bean，id是Bean的名字，class是Bean的地址
<bean id="SimpleBean", class="com.origin.SimpleBean>
```


这样之后，Spring容器就知道有哪些Bean需要管理，以及如何创建这些Bean。这个过程叫注册Bean。



### 2.创建Bean实例

重点放在这句话上面
```java
//反射构造
        SimpleBean bean = context.getBean(SimpleBean.class);
```


调用链如下

```
AbstractApplicationContext.getBean()
├── getBeanFactory().getBean()
│   ├── doGetBean()
│   │   ├── 检查单例缓存
│   │   ├── 创建Bean（如果不存在）
│   │   │   ├── createBean()
│   │   │   │   ├── 解析Bean类
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
│   │   └── 返回Bean实例
│   └── 类型转换（如果需要）
└── 返回Bean
```

好吧这个图可以不看，因为我也没看，简单来说就是`getBean()`先检查缓存是否已经有实例，若无，则`doGetBean`创建实例。
接下来就一直往下调用了，中途最关键的是这个Java反射API

```java
@CallerSensitive
@ForceInline
// Java反射API
public T newInstance(Object... initargs) {
    // 获取调用者并执行实例化
    Class<?> caller = override ? null : Reflection.getCallerClass();
    return newInstanceWithCaller(initargs, !override, caller);
}
```

这里的caller是Spring拿到的需要创建的类，然后就会调用`newInstanceWithCaller`来根据构造函数参数`initargs`来匹配构造函数


在这段代码中：
- **`initargs`**：这就是传递给构造器的参数，Spring 会根据情况填充这个数组。
- **`Reflection.getCallerClass()`**：用于获取调用者类的信息，通常与权限和安全性相关。它确保反射的调用是在合适的上下文中进行的。

#### 2.1 **Spring 选择构造器**

Spring 首先通过配置或上下文选择合适的构造器（无参或有参）。在 `InstantiationStrategy`（默认实现是 `SimpleInstantiationStrategy`）中，Spring 会根据条件选择构造器：

```java
constructorToUse.setAccessible(true);
return (T) constructorToUse.newInstance(args);
```

- **`constructorToUse`**：这是 Spring 选择的构造器。
- **`args`**：这是传递给构造器的参数，可以是一个空数组（无参构造器）或填充了依赖项的数组（有参构造器）。


如果选择的是无参构造器，Spring 会传递一个空的参数数组：

```java
constructorToUse.newInstance();  // 等价于 newInstance(new Object[0])
```
此时，`initargs` 的长度为 0，反射机制会调用无参构造器。

如果选择的是有参构造器，Spring 会把已经准备好的参数放到 `Object[] args` 数组中，传递给 `newInstance`：

```java
constructorToUse.newInstance(args);
```
总之，Spring会自动选择出一个合适的构造函数，并准备好参数，使用 `newInstance(Object... initargs)`（底层通过反射实现）来创建对象实例。

#### 依赖注入
简单来说就是Spring 看`@Autowired`或者构造函数的参数等来看是不是需要注入依赖。

比如
```java
Class A
{
    @Autowired
    Private B b;
}
```
这里实例化类A的时候需要先注入B

#### 调用`init()`方法
`init()`方法一般是一些准备工作


#### 放入容器中
完成创建后，Spring会把它缓存起来（如单例Bean）。



## 依赖注入的顺序：两个例子

### 第一个例子

这里专门研究依赖注入，我们很好奇，如果是以下的结构

```java
Class A
{
    @Autowired
    Private B b;
}
```
A和B的的构造函数,初始化方法和销毁方法的调用顺序是什么样
下面是验证代码

```java
package com.origin;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;  // 缺少这个导入
@Component
class SimpleBean {
    @Autowired
    private DependentBean dependentBean;

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

@Component
class DependentBean {

    public DependentBean() {

        System.out.println("1. DependentBean 构造函数被调用");
    }

    @PostConstruct
    public void init() {

        System.out.println("2. DependentBean 初始化方法被调用");
    }

    @PreDestroy
    public void destroy() {
        
        System.out.println("3. DependentBean 销毁方法被调用");
    }
}


public class Main {
    public static void main(String[] args) {

        AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");
        
        //反射构造
        SimpleBean bean = context.getBean(SimpleBean.class);

        context.close();
    }
}

```

下面是输出
```
1. DependentBean 构造函数被调用
2. DependentBean 初始化方法被调用
1. SimpleBean 构造函数被调用
2. SimpleBean 初始化方法被调用
3. SimpleBean 销毁方法被调用
3. DependentBean 销毁方法被调用
```

逻辑是先调用需要注入的Bean的构造函数和初始化方法，销毁方法和创建的顺序是相反的。

我们认为Spring构造Bean的时候会先去找出依赖的Bean，把依赖的Bean构造，初始化之后才会，继续原来Bean的构造和初始化。

但是接下来的例子打破了这种认识

### 第二个例子

第二个例子仅仅对第一个例子做了全文替换`SimpleBean->A`，`DependentBean->B`,输出的顺序发生了变化

```java
package com.origin;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;  // 缺少这个导入
@Component
class A {
    @Autowired
    private B b;

    public A() {

        System.out.println("1. A 构造函数被调用");
    }

    @PostConstruct
    public void init() {

        System.out.println("2. A 初始化方法被调用");
    }

    @PreDestroy
    public void destroy() {
        
        System.out.println("3. A 销毁方法被调用");
    }
}

@Component
class B {

    public B() {

        System.out.println("1. B 构造函数被调用");
    }

    @PostConstruct
    public void init() {

        System.out.println("2. B 初始化方法被调用");
    }

    @PreDestroy
    public void destroy() {
        
        System.out.println("3. B 销毁方法被调用");
    }
}


public class Main {
    public static void main(String[] args) {

        AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");
        
        //反射构造
        A bean = context.getBean(A.class);

        context.close();
    }
}
```

输出为
```
1. A 构造函数被调用
1. B 构造函数被调用
2. B 初始化方法被调用
2. A 初始化方法被调用
3. A 销毁方法被调用
3. B 销毁方法被调用
```
如果按照第一个例子的输出，应该是先调用B的构造函数和初始化方法才对。


这是为什么呢？

### 问题：为什么依赖注入Bean的方法调用顺序逻辑会变动？

我做的事是：


* 原始类名是 `SimpleBean` 和 `DependentBean`；
* 后来做了文本替换，类名变成了 `A` 和 `B`；
* 结果输出顺序从：

```text
1. DependentBean 构造函数被调用
2. DependentBean 初始化方法被调用
1. SimpleBean 构造函数被调用
2. SimpleBean 初始化方法被调用
```

变成了：

```text
1. A 构造函数被调用
1. B 构造函数被调用
2. B 初始化方法被调用
2. A 初始化方法被调用
```

问了GPT4o

真相是：**扫描注册顺序决定了谁先触发构造**

```java
 AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");
```

在 **字段注入** 时，Spring 并不会先去把 `B` 构造好，再去构造 `A`。真正逻辑是这样的：

> Spring 会先去创建容器里注册顺序靠前的 Bean，比如 `A`，然后在创建 `A` 的时候，如果发现它依赖 `B`，才会“顺便”构造 `B`。

这意味着：

* 如果 **A 被先扫描到、先注册**，Spring 就会**先尝试创建 A** → 发现依赖 B → **然后再去创建 B**；
* 所以日志就会是：

  ```
  A 构造函数被调用
  B 构造函数被调用
  B 初始化方法被调用
  A 初始化方法被调用
  ```

所以
```java
 AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");
```
这行代码运行之后，`A`和`B`实际注册的顺序为
```text
[A,B]
```
换句话说是A在B前。

之前`SimpleBean`和`DependentBean`的注册顺序是
```text
[DependentBean,SimpleBean]
```
所以才会导致这种差异

**如何验证这种说法**

**方法：加入自定义BeanFactoryPostProcessor打印注册顺序**
```java
@Component
class MyBeanFactoryPostProcessor implements BeanFactoryPostProcessor{
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory factory) {
        System.out.println("Spring 注册的 Bean 顺序：");
        for (String name : factory.getBeanDefinitionNames()) {
            System.out.println("  -> " + name);
        }
    }
}
```

第一个例子

```
Spring 注册的 Bean 顺序：
  -> ...
  -> dependentBean
  -> myBeanFactoryPostProcessor
  -> simpleBean
```

第二个例子

```
Spring 注册的 Bean 顺序：
  -> ...
  -> a
  -> b
  -> myBeanFactoryPostProcessor
```
可以看到替换Bean的名字之后，注册顺序确实发生了变化

### 新的问题：为什么简单的文本替换会导致注册的Bean的顺序发生变化？

**猜想：实际上Bean的注册顺序是按照名称字母排序（字典排序）！**

**验证：创建一些不同名字的Bean，并且打乱代码里面的前后顺序**

```java
@Component
class Edho { ... }

@Component
class Alpha { ... }

@Component
class Beta { ... }

@Component
class Charlie { ... }

@Component
class Delta { ... }

@Component
class Echo { ... }

@Component
class Foxtrot { ... }

```

打印结果

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

符合预期


**问题：Spring源码哪一部分体现了按字典排序**


```java
new AnnotationConfigApplicationContext("com.example")
```
在第一句话的调用链里面，

* 在 `ClassPathScanningCandidateComponentProvider` 里加载类（通过 `MetadataReader`）时，**并没有排序操作**；
* 所以 Bean 的注册顺序 **不是 Spring 主动排序的结果**；
* 看到的顺序是因为它调用的底层方法，比如 `File.listFiles()` 或 `JarFile.entries()`，这些**返回的本身就是近似字典序**。但严格来说，并不保证是完全的字典序。
* `File.listFiles()` 是 Java 的文件系统 API，用于列出指定目录下的文件和子目录。
* 在大多数操作系统（如 Windows、Linux、macOS）中，文件系统的目录遍历通常会返回按**文件名字典序**（lexicographical order）排序的结果，但这并不是 Java 官方 API 文档所保证的行为。具体顺序取决于底层文件系统的实现。



### **为什么销毁时是注册顺序的反过来？**



想象现在有两个 Bean：

* `A` 依赖于 `B`（`A` 用 `B` 做事情）
* 所以 Spring 在创建时先构造 `B`，然后构造 `A`

也就是说：

> **谁依赖别人，谁就后创建。**

---

### **销毁时反过来：先销毁 A，再销毁 B**


 **举个例子（真实场景）**

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

如果 Spring 销毁顺序是：

* **先销毁 ConnectionManager**
* 再销毁 UserService

那 UserService 在 `@PreDestroy` 里如果还想做点数据库操作（比如写日志）就会出错，因为连接已经没了。

---

### **所以：Spring 必须保证依赖关系**

1. 先销毁 **用别人的那一方**（UserService）；
2. 最后销毁 **被依赖的那一方**（ConnectionManager）。

---