import turtle
import threading
import random

def draw_snowfall(num_snowflakes=250):
    snowfall_turtle = turtle.Turtle()
    snowfall_turtle.hideturtle()
    snowfall_turtle.speed(0)
    snowfall_turtle.color("white")
    snowfall_turtle.penup()

    for _ in range(num_snowflakes):
        x = random.uniform(-300, 300)
        y = random.uniform(-300, 300)
        snowfall_turtle.goto(x, y)
        snowfall_turtle.dot(random.uniform(1, 3))

def koch_snowflake(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_snowflake(t, order - 1, size / 3)
            t.left(angle)

def draw_koch_snowflake(order, size=300):
    snowflake_turtle = turtle.Turtle()
    snowflake_turtle.penup()
    snowflake_turtle.goto(-size / 2, size / 4)
    snowflake_turtle.pendown()
    
    snowflake_turtle.color("white")
    snowflake_turtle.speed(15)
    snowflake_turtle.width(2)

    for _ in range(3):
        koch_snowflake(snowflake_turtle, order, size)
        snowflake_turtle.right(120)

def main():
    recursion_depth = int(input("Enter the recursion depth: "))

    screen = turtle.Screen()
    screen.bgcolor("#add8e6") 

    draw_snowfall_thread = threading.Thread(target=draw_snowfall)
    draw_koch_snowflake_thread = threading.Thread(target=draw_koch_snowflake, args=(recursion_depth, 300))

    draw_snowfall_thread.start()
    screen.ontimer(draw_koch_snowflake_thread.start, 1000)  

    screen.listen()
    screen.onkey(screen.bye, "q")  
    screen.mainloop()

if __name__ == "__main__":
    main()
