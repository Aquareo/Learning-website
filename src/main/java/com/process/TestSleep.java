package com.process;

class MyRunnable implements Runnable{

    private static int ticket=30;


    //能否访问
    private static boolean flag = false;

    private final String name;

    public MyRunnable(String name) {
        this.name = name;
    }


    @Override
    public void run() {
        while (ticket > 0) {
            // 加入随机延迟，放大问题
            try {
                Thread.sleep((long) (Math.random() * 10));
                //Thread.sleep(100); // 模拟处理时间
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            
            while(flag && ticket > 0);
            
            // 进入临界区
            flag=true;

            if(ticket <= 0) {
                flag = false; // 释放锁
                return; // 没票了，退出
            }

            // 模拟买票
            System.out.println(name + "买了第" + ticket-- + "张票");

            // 退出临界区
            flag = false;
        }
    }
}


public class TestSleep {
    public static void main(String[] args) {
        // 创建多个售票点
        MyRunnable r1 = new MyRunnable("售票点1-小明");
        MyRunnable r2 = new MyRunnable("售票点2-老师");
        MyRunnable r3 = new MyRunnable("售票点3-小红");
        MyRunnable r4 = new MyRunnable("售票点4-保安");
        
        Thread t1 = new Thread(r1);
        Thread t2 = new Thread(r2);
        Thread t3 = new Thread(r3);
        Thread t4 = new Thread(r4);


        t1.start();
        t2.start();
        t3.start();
        t4.start();
    }
}
