def main():
    print("Hello from xarm-python-controls!")
    ball_positions = ((-1, -1, 1, 1, 1, -1, -1), 
                    (-1, -1, 1, 1, 1, -1, -1), 
                    (1, 1, 1, 1, 1, 1, 1), 
                    (1, 1, 1, 0, 1, 1, 1), 
                    (1, 1, 1, 1, 1, 1, 1), 
                    (-1, -1, 1, 1, 1, -1, -1), 
                    (-1, -1, 1, 1, 1, -1, -1))
    print(ball_positions[1][2])


if __name__ == "__main__":
    main()
