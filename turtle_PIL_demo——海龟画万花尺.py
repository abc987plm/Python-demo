import turtle, argparse, sys, math, random
import numpy as np
from PIL import Image
from datetime import datetime


# a class that draws a Spirograph 画螺旋描记器的类
class Spiro:
    # constructor 构造函数
    def __init__(self, xc, yc, col, R, r, l):

        # create the turtle object 创建Turtle对象
        self.t = turtle.Turtle()
        # set the cursor shape 设置光标形状
        self.t.shape('turtle')
        # set the step in degrees 设置以step为单位步进量
        self.step = 1
        # set the drawing complete flag 设置绘图完成标志
        self.drawingComplete = False

        # set the parameters 设置参数
        self.setparams(xc, yc, col, R, r, l)

        # initialize the drawing  初始化绘图
        self.restart()

    # set the parameters
    def setparams(self, xc, yc, col, R, r, l):
        # the Spirograph parameters 螺旋仪参数
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        # reduce r/R to its smallest form by dividing with the GCD 用gcd除法将r/R减小到最小值
        gcdVal = math.gcd(self.r, self.R)
        self.nRot = self.r//gcdVal
        # get ratio of radii  得到半径比
        self.K = r/float(R)
        # set the color 设置颜色
        self.t.color(*col)
        # store the current angle  存储当前角度
        self.a = 0

    # restart the drawing  重新启动绘图
    def restart(self):
        # set the flag  设置标志
        self.drawingComplete = False
        # show the turtle 出示海龟
        self.t.showturtle()
        # go to the first point  转到第一点
        self.t.up()
        R, k, l = self.R, self.K, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    # draw the whole thing 画出整件事
    def draw(self):
        # draw the rest of the points  画其余的点
        R, k, l = self.R, self.K, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
            # drawing is now done so hide the turtle cursor  绘图完成，隐藏乌龟光标
            self.t.hideturtle()

        # update by one step  一步更新
    def update(self):
        # skip the rest of the step if done  完成后跳过其余步骤
        if self.drawingComplete:
            return
        # increment the angle 增加角度
        self.a += self.step
        # draw a step  画出一个台阶
        R, k, l = self.R, self.K, self.l
        # set the angle  设置角度
        a = math.radians(self.a)
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        # if drawing is complete, set the flag 如果绘图完成，设置标志
        if self.a >= 360*self.nRot:
            self.drawingComplete = True
            # drawing is now done so hide the turtle cursor
            self.t.hideturtle()

    # clear everything
    def clear(self):
        self.t.clear()

# a class for animating Spriographs  一个用来制作spriograph动画的类
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # set the timer value in milliseconds 以毫秒为单位设置计时器值
        self.deltaT = 10
        # get the window dimensions  获取窗口尺寸
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # create the Spiro objects  创建spiro对象
        self.spiros = []
        for i in range(N):
            # generate random parameters  生成随机参数
            rparams = self.genRandomParams()
            # set the spiro parameters  设置spiro参数
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
            # call timer  通话计时
            turtle.ontimer(self.update, self.deltaT)

    # restart spiro drawing  重新启动Spiro绘图
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters  生成随机参数
            rparms = self.genRandomParams()
            # set the spiro parameters  设置spiro参数
            spiro.setparams(*rparms)
            # restart drawing  再启动绘图
            spiro.restart()

    # geberate random parameters  Geberate随机参数
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(),random.random(),random.random())
        return (xc, yc, col, R, r, l)



    def update(self):
        # update all spiros  更新所有spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed spiros  完成spiros计数
            if spiro.drawingComplete:
                nComplete += 1
        # restart if all spiros are complete  如果所有Spiros都已完成，则重新启动
        if nComplete == len(self.spiros):
            self.restart()
        # call the timer  叫计时器
        turtle.ontimer(self.update, self.deltaT)

    # toggle turtle cursor on and off  打开和关闭海龟光标
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

# save drawings as PNG files  将图形另存为PNG文件
def saveDrawing():
    # hide the turtle cursor  隐藏海龟光标
    turtle.hideturtle()
    # generate unique filenames  生成唯一文件名
    dateStr = (datetime.now()).strftime('%d%b%Y-%H%M%S')
    fileName = 'spiro-' + dateStr
    print('saving drawing to %s.eps/png' % fileName)
    # get the tkinter canvas  获取tkinter画布
    canvas = turtle.getcanvas()
    # save the drawing as a postscipt image  将绘图另存为PostCipt图像
    canvas.postscript(file = fileName + '.eps')
    # use the Pillow module to convert the poscript image file to PNG 使用Pillow模块将poscript图像文件转换为png
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')
    # show the turtle cursor  显示海龟光标
    turtle.showturtle()

# main() function
def main():
    # use sys.argv if needed 如果需要，使用sys.argv
    print('generating spirograph...')
    # create parser  创建语法分析器
    descStr = """This program draws Spirographs using the Turtle module.
    When run with no arguments, this program draws random Spirographs.
    
    Terminology:
    
    R:radius of outer circle
    r:radius of inner circle
    l:ratio of hole distance to r
    """

    parser = argparse.ArgumentParser(description = descStr)

    # add expected arguments  添加预期参数
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help='The three arguments in sparams:R, r, l.')

    # parse args  解析ARG
    args = parser.parse_args()

    # set the width of the drawing window to 80 percent of the screen width  将绘图窗口的宽度设置为屏幕宽度的80%
    turtle.setup(width=0.8)

    # set the cursor shape to turtle 将光标形状设置为Turtle
    turtle.shape('turtle')

    # set the title to Spirographs!  将标题设置为Spirographs！
    turtle.title('Spirographs!')
    # add the key handler to save our drawings 添加密钥处理程序以保存绘图
    turtle.onkey(saveDrawing, 's')
    # start listening 开始听
    turtle.listen()

    # hide the main turtle cursor  隐藏海龟主光标
    turtle.hideturtle()

    # check for any arguments sent to --sparams and draw the Spirograph
    # 检查是否有任何参数发送到——sparams并绘制Spirograph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw the Spirograph with the given parameters
        # 用给定的参数绘制螺旋仪
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create the animator object 创建动画师对象
        spiroAnim = SpiroAnimator(4)
        # add a key handler to toggle the turtle cursor
        # 添加一个键处理程序以切换海龟光标
        turtle.onkey(spiroAnim.toggleTurtles, 't')
        # add a key handler to restart the animation
        # 添加键处理程序以重新启动动画
        turtle.onkey(spiroAnim.restart, 'space')

    # start the turtle main loop 启动乌龟主回路
    turtle.mainloop()


if __name__ == '__main__':
    main()