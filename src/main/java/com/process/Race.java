package com.process;
//龟兔赛跑

public class Race implements Runnable {

    private static String winner;//赢家


    @Override
    public void run() {
        String name = Thread.currentThread().getName();
        for (int i = 0; i <= 100; i++) {

            boolean end=end(i);
            if (end) {
                break; //如果比赛结束，退出循环
            }
            System.out.println(name + "跑了" + i + "步");

        }
        System.out.println(name + "到达终点");
    }


    public static boolean end(int steps)
    {
        if(winner != null)
        {
            return true; //比赛已经结束
        }
        if(steps >= 100)
        {
            winner = Thread.currentThread().getName();
            System.out.println("赢家是:" + winner);
            return true; //比赛已经结束
        }
        return false; //比赛还在进行中
    }


    public static void main(String[] args)
    {
        Thread t1=new Thread(new Race(),"兔子");
        Thread t2=new Thread(new Race(),"乌龟");

        t1.start();
        t2.start();
    }


}