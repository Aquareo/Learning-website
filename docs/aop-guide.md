# Spring AOP 核心知识点

## 1. AOP基础概念

### 1.1 什么是AOP
AOP(Aspect Oriented Programming)面向切面编程，是一种编程范式，它允许你把横切关注点(如日志、性能统计、安全)从业务逻辑中分离出来。

### 1.2 为什么要用AOP
- 代码复用
- 解耦合
- 集中管理
- 提高可维护性

### 1.3 核心术语
1. **切面(Aspect)**：横切关注点的模块化，比如日志功能
2. **连接点(JoinPoint)**：程序执行过程中的某个特定点，如方法调用
3. **切点(Pointcut)**：匹配连接点的表达式
4. **通知(Advice)**：切面在特定连接点执行的动作
5. **目标对象(Target)**：被切面通知的对象
6. **AOP代理(AOP Proxy)**：AOP框架创建的代理对象

## 2. Spring AOP实现方式

### 2.1 两种代理方式
1. **JDK动态代理**
   - 针对有接口的类
   - 生成接口的代理类
```java
public interface UserService {
    void addUser();
}
// JDK会生成UserService的代理实现类
```

2. **CGLIB代理**
   - 针对没有接口的类
   - 通过继承被代理类来实现
```java
public class UserService {
    public void addUser() {}
}
// CGLIB会生成UserService的子类
```

### 2.2 常用注解
1. **@Aspect**：声明切面类
2. **@Pointcut**：定义切点
3. **@Before**：前置通知
4. **@After**：后置通知
5. **@AfterReturning**：返回通知
6. **@AfterThrowing**：异常通知
7. **@Around**：环绕通知

### 2.3 切点表达式
```java
execution(modifiers-pattern? ret-type-pattern declaring-type-pattern?name-pattern(param-pattern) throws-pattern?)
```
例子：
```java
// 所有public方法
execution(public * *(..))

// 所有service包下的方法
execution(* com.example.service.*.*(..))

// 特定方法名
execution(* com.example.service.UserService.addUser(..))
```

## 3. 面试常见问题

### 3.1 AOP和OOP的区别？
- OOP是纵向继承机制，关注业务逻辑单元的封装
- AOP是横向切面机制，关注多个类的共同行为

### 3.2 JDK动态代理和CGLIB代理的区别？
1. **JDK动态代理**：
   - 必须有接口
   - 生成的代理类实现接口
   - 通过反射调用方法
   - JDK原生支持，性能相对较好

2. **CGLIB代理**：
   - 不需要接口
   - 通过继承目标类
   - 通过方法拦截
   - 需要额外依赖，但功能更强大

### 3.3 Spring AOP和AspectJ的区别？
1. **Spring AOP**：
   - 运行时增强
   - 基于代理
   - 只支持方法级别的切面
   - 轻量级、使用简单

2. **AspectJ**：
   - 编译时增强
   - 修改字节码
   - 支持字段、方法、构造器等多种切入点
   - 功能强大但较复杂

### 3.4 实际应用场景
1. **事务管理**：@Transactional
2. **权限控制**：@PreAuthorize
3. **缓存**：@Cacheable
4. **日志记录**
5. **性能监控**
6. **参数校验**
7. **异常处理**

### 3.5 执行顺序
正常情况：
```
Around(前) -> Before -> 方法执行 -> Around(后) -> After -> AfterReturning
```

异常情况：
```
Around(前) -> Before -> 方法执行 -> Around(异常) -> After -> AfterThrowing
```

## 4. 最佳实践

### 4.1 切面优先级
使用@Order注解控制多个切面的优先级：
```java
@Aspect
@Order(1)  // 数字越小优先级越高
@Component
public class LoggingAspect {
}
```

### 4.2 性能考虑
- 避免过多切面
- 切点表达式要精确
- 合理使用环绕通知
