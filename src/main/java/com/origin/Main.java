package com.origin;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.BeanFactoryPostProcessor;
import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.stereotype.Component;

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
class Alpha {
    public Alpha() {
        System.out.println("Alpha 构造");
    }

    @PostConstruct
    public void init() {
        System.out.println("Alpha 初始化");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("Alpha 销毁");
    }
}

@Component
class Beta {

    public Beta() {
        System.out.println("Beta 构造");
    }

    @PostConstruct
    public void init() {
        System.out.println("Beta 初始化");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("Beta 销毁");
    }
}

@Component
class Charlie {
    @Autowired
    private Alpha alpha;

    public Charlie() {
        System.out.println("Charlie 构造");
    }

    @PostConstruct
    public void init() {
        System.out.println("Charlie 初始化");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("Charlie 销毁");
    }
}

@Component
class Delta {
    public Delta() {
        System.out.println("Delta 构造");
    }

    @PostConstruct
    public void init() {
        System.out.println("Delta 初始化");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("Delta 销毁");
    }
}

@Component
class Echo {
    public Echo() {
        System.out.println("Echo 构造");
    }

    @PostConstruct
    public void init() {
        System.out.println("Echo 初始化");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("Echo 销毁");
    }
}
@Component
class Foxtrot {
    public Foxtrot() {
        System.out.println("Foxtrot 构造");
    }

    @PostConstruct
    public void init() {
        System.out.println("Foxtrot 初始化");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("Foxtrot 销毁");
    }
}

@Component
class Edho {
    public Edho() {
        System.out.println("Edho 构造");
    }

    @PostConstruct
    public void init() {
        System.out.println("Edho 初始化");
    }

    @PreDestroy
    public void destroy() {
        System.out.println("Edho 销毁");
    }
}



public class Main {
    public static void main(String[] args) {

        AnnotationConfigApplicationContext context = 
            new AnnotationConfigApplicationContext("com.origin");
   
        context.close();
    }
}
