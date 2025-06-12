package com.aop;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.stereotype.Component;


// 目标类
@Component
class TargetService {
    public void doSomething() {
        System.out.println("==> 执行业务逻辑 doSomething");
    }
}

// 切面类
@Aspect
@Component
class LogAspect {
    // 前置通知
    @Before("execution(* com.aop.TargetService.doSomething(..))")
    public void before(JoinPoint joinPoint) {
        System.out.println("==> AOP 前置通知: " + joinPoint.getSignature());
    }

    // 后置通知
    @After("execution(* com.aop.TargetService.doSomething(..))")
    public void after(JoinPoint joinPoint) {
        System.out.println("==> AOP 后置通知: " + joinPoint.getSignature());
    }
}
// 启用 AOP 自动代理
@EnableAspectJAutoProxy
// 指定扫描的包路径
@ComponentScan("com.aop")
public class Main {
    public static void main(String[] args) {
        // 创建 Spring 容器
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(Main.class);
        // 从容器中获取 TargetService 的代理对象
        TargetService service = context.getBean(TargetService.class);
        // 调用方法，观察 AOP 的行为
        service.doSomething();
        // 关闭容器
        context.close();
    }
}

