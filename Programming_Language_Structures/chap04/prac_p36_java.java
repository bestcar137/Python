public class CircleArea {
    public static void main(String[] args) {
        final double PI = 3.14; // 원주율을 상수로 선언
        double radius = 10; // 원의 반지름
        double circleArea = 0;

        circleArea = PI * radius * radius;  // 원의 면적 계산
        System.out.print("Circle Area = ");
        System.out.println(circleArea);
    }
}