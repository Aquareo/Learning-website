package com.process;


interface Ilike{
        void lambda();
    }

interface Love
{
    void fun(int a);
}

// 1.普通类
class Like1 implements Ilike {
    @Override
    public void lambda() {
        System.out.println("I like lambda1");
    }
}

public class Lambda {

    //2.静态内部类
    static class Like2 implements Ilike {
        @Override
        public void lambda() {
            System.out.println("I like lambda2");
        }
    }
    

    public static void main(String[] args) {
        Ilike like=new Like1();
        like.lambda();

        like=new Like2();
        like.lambda();

        //3.局部内部类
        class Like3 implements Ilike {
            @Override
            public void lambda() {
                System.out.println("I like lambda3");
            }
        }
        like=new Like3();
        like.lambda();


        //4.匿名内部类
        like=new Ilike() {
            @Override
            public void lambda() {
                System.out.println("I like lambda4"); 
            }
        };
        like.lambda();

        
        //5.使用Lambda表达式
        like = () -> System.out.println("I like lambda5");
        like.lambda();
         
        
        //6.使用Lambda表达式，变种
        //Love love = (int a) -> System.out.println("I like lambda"+a);
        //love.fun(6);

        //7.使用Lambda表达式，变种
        Love love = a -> {System.out.println("I like lambda"+a);};
        love.fun(6);
    } 
}
