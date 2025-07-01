package com.proxy;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

class TestInvocationHandler implements InvocationHandler {

    /**
     * 目标对象
     */
    private final Object target;

    public TestInvocationHandler(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {

        //前置逻辑：打印方法调用日志
        System.out.println("调用方法名称为: " + method.getName());

        // 调用目标对象的方法
        Object result = method.invoke(target, args);

        //后置逻辑：打印方法调用结束日志
        System.out.println("After method: " + method.getName());


        return result;
    }
}

interface UserService {
    void doSomething();
}

class UserServiceImpl implements UserService {
    @Override
    public void doSomething() {
        System.out.println("执行业务逻辑");
    }
}
public class Main {
    public static void main(String[] args) {
        // 创建目标对象
        UserService target = new UserServiceImpl();

        // 创建InvocationHandler
        InvocationHandler handler = new TestInvocationHandler(target);

        // 创建代理对象
        UserService proxy = (UserService) java.lang.reflect.Proxy.newProxyInstance(
                target.getClass().getClassLoader(),
                target.getClass().getInterfaces(),
                handler
        );

        // 创建代理对象
        //UserService proxy = (UserService) java.lang.reflect.Proxy.newProxyInstance(
        //        handler.getClass().getClassLoader(),
        //        target.getClass().getInterfaces(),
        //        handler
        //);
        

        // 调用代理对象的方法
        proxy.doSomething();
    }
    
}
