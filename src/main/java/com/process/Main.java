package com.process;

import  java.io.File;
import  java.io.IOException;
import java.net.URL;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import org.apache.commons.io.FileUtils;


//Runnable接口的run()方法没有返回值，也不能抛出受检异常。Callable接口的call()方法可以有返回值，也可以抛出异常。

class MyThread extends Thread {
    final private String url;
    final private String name;

    public MyThread(String url, String name) {
        this.url = url;
        this.name = name;
    }

    @Override
    public void run() {
        webDownloader wd = new webDownloader();
        wd.downloader(url, name);
        System.out.println("下载了文件名为:" + name);
    }
}

class MyRunneable implements Runnable{
    final private String url;
    final private String name;

    public MyRunneable(String url, String name) {
        this.url = url;
        this.name = name;
    }

    @Override
    public void run()
    {
        webDownloader wd = new webDownloader();
        wd.downloader(url, name);
        System.out.println("下载了文件名为: "+ name);
    }
}

class MyCallable implements Callable<Boolean>
{
    final private String url;
    final private String name;

    public MyCallable(String url, String name) {
        this.url = url;
        this.name = name;
    }

    @Override
    public Boolean call() {
        webDownloader wd = new webDownloader();
        wd.downloader(url, name);
        System.out.println("下载了文件名为: " + name);
        return true;
    }
}

class webDownloader {
    public void downloader(String url, String name) {
        try {
            FileUtils.copyURLToFile(
                new URL(url),
                new File(name)
            );
        } catch (IOException e) {
            e.printStackTrace();
        } 
    }
}

public class Main {
    public static void main(String[] args) {

        //1.用Thread类的子类来实现多线程

        MyThread t1 = new MyThread("https://img-s.msn.cn/tenant/amp/entityid/AA1Hk338.img?w=768&h=482&m=6", "1.jpg");
        MyThread t2 = new MyThread("https://img-s.msn.cn/tenant/amp/entityid/AA1HhWxW.img?w=584&h=328&m=6", "2.jpg");
        MyThread t3 = new MyThread("https://img-s.msn.cn/tenant/amp/entityid/AA1HhUci.img?w=584&h=328&m=6", "3.jpg");
        t1.start();
        t2.start();
        t3.start();

        //2.用Runnable接口来实现多线程
        Thread t4=new Thread(new MyRunneable("https://img-s.msn.cn/tenant/amp/entityid/AA1HhUci.img?w=584&h=328&m=6", "4.jpg"));
        Thread t5=new Thread(new MyRunneable("https://img-s.msn.cn/tenant/amp/entityid/AA1HhWxW.img?w=584&h=328&m=6", "5.jpg"));
        Thread t6=new Thread(new MyRunneable("https://img-s.msn.cn/tenant/amp/entityid/AA1Hk338.img?w=768&h=482&m=6", "6.jpg"));
        t4.start();
        t5.start();
        t6.start();

        //3.用Callable来实现多线程
        
        //为什么还要用Future?
        //Thread只能直接执行Runnable对象，不能直接执行Callable对象。
        //所以，java提供了一个"适配器"---FutureTask,他即是Runnable又是Callable。
        //你可以把callable交给FutureTask来执行，再把FutureTask作为Runnable交给Thread来启动。

        int nThread=3;

        ExecutorService pool = Executors.newFixedThreadPool(nThread); // 固定线程池，数量根据需求调节

        Future<Boolean>[] futures = new Future[nThread];

        futures[0] = pool.submit(new MyCallable("https://img-s.msn.cn/tenant/amp/entityid/AA1Hk338.img?w=768&h=482&m=6", "7.jpg"));
        futures[1] = pool.submit(new MyCallable("https://img-s.msn.cn/tenant/amp/entityid/AA1HhWxW.img?w=584&h=328&m=6", "8.jpg"));        
        futures[2] = pool.submit(new MyCallable("https://img-s.msn.cn/tenant/amp/entityid/AA1HhUci.img?w=584&h=328&m=6", "9.jpg"));

        for(Future<Boolean> f : futures) 
        {
            try{
                f.get(); // 等待任务完成
            } catch (Exception e) {
                e.printStackTrace();
            }

        }
        pool.shutdown(); // 关闭线程池
        
    }
}
