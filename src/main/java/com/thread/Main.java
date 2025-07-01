package com.thread;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.FutureTask;
import java.util.concurrent.locks.ReentrantLock;

public class Main {
    public static void main(String[] args) {
        // 1. 展示三种创建线程的方式
        // 方式1：继承Thread类
        Thread thread1 = new Thread() {
            @Override
            public void run() {
                System.out.println("方式1：继承Thread类 - " + Thread.currentThread().getName());
            }
        };

        // 方式2：实现Runnable接口
        Thread thread2 = new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("方式2：实现Runnable接口 - " + Thread.currentThread().getName());
            }
        });

        // 方式3：使用Callable和Future
        FutureTask<String> futureTask = new FutureTask<>(new Callable<String>() {
            @Override
            public String call() throws Exception {
                return "方式3：实现Callable接口 - " + Thread.currentThread().getName();
            }
        });
        Thread thread3 = new Thread(futureTask);

        thread1.start();
        thread2.start();
        thread3.start();

        // 2. 线程同步示例 - 银行账户
        BankAccount account = new BankAccount(1000);
        Thread withdrawThread1 = new Thread(() -> {
            account.withdraw(800);
        });
        Thread withdrawThread2 = new Thread(() -> {
            account.withdraw(800);
        });

        withdrawThread1.start();
        withdrawThread2.start();

        // 3. 生产者-消费者示例
        BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(5);
        Thread producer = new Thread(new Producer(queue));
        Thread consumer = new Thread(new Consumer(queue));

        producer.start();
        consumer.start();

        // 4. 线程池示例
        ExecutorService executor = Executors.newFixedThreadPool(3);
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("线程池任务" + taskId + " 被线程" + 
                    Thread.currentThread().getName() + "执行");
            });
        }
        executor.shutdown();
    }
}

// 银行账户类 - 展示同步
class BankAccount {
    private double balance;
    private ReentrantLock lock = new ReentrantLock();

    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }

    public void withdraw(double amount) {
        lock.lock();
        try {
            if (balance >= amount) {
                System.out.println("准备取款: " + amount);
                Thread.sleep(100); // 模拟处理时间
                balance -= amount;
                System.out.println("取款成功，当前余额: " + balance);
            } else {
                System.out.println("余额不足，取款失败");
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
}

// 生产者类
class Producer implements Runnable {
    private BlockingQueue<Integer> queue;

    public Producer(BlockingQueue<Integer> queue) {
        this.queue = queue;
    }

    @Override
    public void run() {
        try {
            for (int i = 0; i < 10; i++) {
                System.out.println("生产者生产: " + i);
                queue.put(i);
                Thread.sleep(100);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

// 消费者类
class Consumer implements Runnable {
    private BlockingQueue<Integer> queue;

    public Consumer(BlockingQueue<Integer> queue) {
        this.queue = queue;
    }

    @Override
    public void run() {
        try {
            while (true) {
                Integer value = queue.take();
                System.out.println("消费者消费: " + value);
                Thread.sleep(200);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
