package com.wiring;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.BeanFactoryPostProcessor;
import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.stereotype.Component;  // 缺少这个导入


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

@Component
class SimpleBean {
        static {
        System.out.println("SimpleBean 类加载");
    }
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
        static {
        System.out.println("DependentBean 类加载");
    }
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
            new AnnotationConfigApplicationContext("com.wiring");
        
        //反射构造
        SimpleBean bean = context.getBean(SimpleBean.class);

        context.close();
    }
}
