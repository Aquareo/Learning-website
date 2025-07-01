package com.process;


//多个线程同时操作一个对象：买火车票



public class Ticket implements Runnable
{
    //火车票数
    private  int ticket = 10;

    @Override
    public void run()
    {   
        while (true) { 
            if(ticket<=0)break;
            else
            {   
                try
                {
                    Thread.sleep(200);
                }
                catch(InterruptedException e)
                {
                    e.printStackTrace();
                }

                
                System.out.println(Thread.currentThread().getName() + "买了第" + ticket-- + "张票");
            }
        }
        
    }

    public static void main(String[] args) 
    {
        Ticket  t = new Ticket();

        new  Thread(t,"小明").start();
        new  Thread(t,"老师").start();
        new  Thread(t,"黄牛").start();
    }    
}
