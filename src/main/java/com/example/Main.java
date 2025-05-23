package com.example;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.stereotype.Component;

@Component
class UserService {
    private final DatabaseConnection database;

    public UserService(DatabaseConnection database) {
        this.database = database;
    }

    public void doSomething() {
        database.connect();
    }
}


@Component
class DatabaseConnection {
    public void connect() {
        System.out.println("Connecting to the database...");
    }
}

public class Main {
    public static void main(String[] args) {
        // 启动Spring容器，并启用组件扫描
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext("com.example");

        // 从容器中获取UserService Bean
        UserService userService = context.getBean(UserService.class);

        // 使用Bean
        userService.doSomething();

        // 关闭Spring容器
        context.close();
    }
}
