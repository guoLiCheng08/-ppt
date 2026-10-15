# coding: utf-8
"""STM32 engineering diagram deck. All figures are editable PowerPoint shapes."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pathlib import Path
from math import sin, pi
import os

r=Presentation();r.slide_width=Inches(13.333);r.slide_height=Inches(7.5)
colors={'bg':'081321','panel':'11263E','panel2':'193653','line':'355875',
'white':'EDF5FC','muted':'ADC2D2','cyan':'52D2E6','orange':'FFC578',
'green':'82E2B5','red':'FF818C','blue':'85ACFD'}
def rgb(c):
 s=colors.get(c,c);return RGBColor(*(int(s[i:i+2],16) for i in (0,2,4)))
def shape(s,x,y,w,h,fill='panel',border='line',rounded=True):
 a=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
 a.fill.solid();a.fill.fore_color.rgb=rgb(fill)
 if border:a.line.color.rgb=rgb(border);a.line.width=Pt(.9)
 else:a.line.fill.background()
 return a
def text(s,t,x,y,w,h,size=13,c='white',bold=False,center=False,font='Microsoft YaHei'):
 a=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
 a.text_frame.word_wrap=True
 a.text_frame.margin_left=Inches(.065);a.text_frame.margin_right=Inches(.065)
 a.text_frame.margin_top=Inches(.02);a.text_frame.margin_bottom=Inches(.01)
 a.text_frame.vertical_anchor=MSO_ANCHOR.MIDDLE
 for i,part in enumerate(str(t).split('\n')):
  p=a.text_frame.paragraphs[0] if i==0 else a.text_frame.add_paragraph()
  p.text=part;p.font.name=font;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=rgb(c)
  if center:p.alignment=PP_ALIGN.CENTER
 return a
def seg(s,x1,y1,x2,y2,c='cyan',thick=1.6):
 a=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2));a.line.color.rgb=rgb(c);a.line.width=Pt(thick)
def arr(s,x1,y1,x2,y2,c='cyan'):
 seg(s,x1,y1,x2,y2,c,2.0);seg(s,x2,y2,x2-.10,y2-.05,c,1.7);seg(s,x2,y2,x2-.10,y2+.05,c,1.7)
def box(s,x,y,w,h,title,detail,fc='panel2'):
 shape(s,x,y,w,h,fc)
 text(s,title,x+.08,y+.10,w-.16,.37,15,'white',True,True)
 text(s,detail,x+.09,y+.53,w-.18,h-.61,10,'muted',False,True)
def new(title,chapter):
 s=r.slides.add_slide(r.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=rgb('bg')
 shape(s,0,0,13.333,.055,'cyan',None,False)
 text(s,'EMBEDDED SYSTEMS  /  '+chapter,.50,.18,11,.27,9,'cyan',True)
 text(s,title,.49,.52,12.30,.63,24,'white',True)
 seg(s,.5,1.27,12.82,1.27,'line',1)
 text(s,'STM32 · ENGINEERING DIAGRAM EDITION',.50,7.12,8.7,.19,8,'muted')
 text(s,f'{len(r.slides):02d}',12.24,7.11,.55,.21,9,'muted',False,True)
 return s
def note(s,t):
 shape(s,.70,6.41,11.98,.45,'panel',None,False)
 text(s,t,.88,6.49,11.65,.30,10,'muted')
def process(title,chapter,items,remarks):
 s=new(title,chapter);n=len(items);cw=(11.8-.28*(n-1))/n
 for i,(name,desc) in enumerate(items):
  x=.76+i*(cw+.28);box(s,x,2.45,cw,1.42,name,desc)
  if i<n-1:arr(s,x+cw,3.13,x+cw+.26,3.13,'orange')
 shape(s,.80,4.53,11.69,.83,'panel2')
 text(s,'核心路径',1.00,4.72,1.14,.38,14,'cyan',True)
 text(s,remarks,2.08,4.62,10.16,.58,13,'white')
 note(s,'工程审查：区分设计假设、芯片规格与示波器实测值；所有图形均可编辑。')
def matrix(title,chapter,headers,rows,remarks):
 s=new(title,chapter);n=len(headers);w=11.86/n;y=1.64
 for j,v in enumerate(headers):
  shape(s,.76+j*w,y,w,.48,'panel2','line',False);text(s,v,.87+j*w,y+.09,w-.13,.30,12,'cyan',True)
 y+=.48
 rowh=min(.72,3.86/len(rows))
 for i,row in enumerate(rows):
  for j,v in enumerate(row):
   shape(s,.76+j*w,y+i*rowh,w,rowh,'panel' if i%2==0 else 'panel2','line',False)
   text(s,v,.87+j*w,y+i*rowh+.05,w-.19,rowh-.10,10 if len(str(v))>30 else 12,'white' if j==0 else 'muted',j==0)
 shape(s,.85,5.72,11.62,.54,'panel2')
 text(s,remarks,1.08,5.81,11.18,.33,12,'white')
 note(s,'条件、指标与阈值仅用于 STM32F103C8T6 的教学设计；投产时需对照具体板卡修订。')
def timing(title,chapter,signals,info,remarks):
 s=new(title,chapter)
 shape(s,.69,1.58,12.00,4.52,'panel')
 text(s,info,.98,1.74,11.32,.35,13,'cyan',True)
 xx=1.48;ww=10.56
 for lane,(name,bits,color) in enumerate(signals):
  yy=2.25+lane*.91
  text(s,name,.85,yy+.19,.65,.28,11,color,True)
  vals=list(bits);N=len(vals)
  for j,v in enumerate(vals):
   x=xx+ww*j/N;end=xx+ww*(j+1)/N
   level=yy+.12 if int(v) else yy+.56
   seg(s,x,level,end,level,color,2.0)
   if j+1<N and vals[j]!=vals[j+1]:seg(s,end,level,end,yy+.12 if int(vals[j+1]) else yy+.56,color,2.0)
  for k in range(N+1):
   x=xx+ww*k/N;seg(s,x,yy-.07,x,yy+.70,'line',.36)
 text(s,remarks,.86,5.45,11.78,.45,12,'white')
 note(s,'时序图为课堂示意；真实建立时间、保持时间、占空比、边沿完整性需测量。')
def branching(title,chapter,root,children,remarks):
 s=new(title,chapter)
 box(s,4.75,1.65,3.84,.86,root,'异常事件 / 顶层失效')
 n=len(children);w=11.84/n
 for i,(a,b) in enumerate(children):
  x=.75+i*w
  box(s,x,3.51,w-.18,1.39,a,b)
  seg(s,6.67,2.51,6.67,2.81,'orange');seg(s,6.67,2.81,x+w/2,2.81,'orange');seg(s,x+w/2,2.81,x+w/2,3.48,'orange')
 shape(s,.83,5.48,11.68,.68,'panel2');text(s,remarks,1.05,5.61,11.22,.36,13,'white')
 note(s,'根因树每一个分支应匹配真实可测信号、重现条件和缺陷处理记录。')
def feedback():
 s=new('速度控制闭环：采样、计算、PWM 更新的位置','SYSTEM CONTROL')
 items=[('r[k]','速度设定'),('Σ','e[k] = r−y'),('PI(z)','离散控制器'),('PWM','TIM2 / 电机驱动'),('电机','速度 / 扭矩')]
 for i,(a,b) in enumerate(items):
  x=.60+i*2.47;box(s,x,2.37,2.22,1.06,a,b)
  if i<4:arr(s,x+2.23,2.88,x+2.44,2.88)
 box(s,7.31,4.58,3.28,.88,'编码器测量','定时器计数 + 速度滤波')
 seg(s,11.12,3.44,11.12,5.12,'orange');seg(s,11.12,5.12,1.82,5.12,'orange');seg(s,1.82,5.12,1.82,3.46,'orange')
 shape(s,.85,5.65,11.7,.59,'panel2')
 text(s,'e[k]=r[k]−y[k]；u[k]=Kp·e[k]+Ki·Ts·Σe[i]；必须添加输出限幅与积分抗饱和',1.00,5.79,11.28,.31,13,'white')
 note(s,'注意 20 kHz PWM 载波与 1 ms 控制更新周期不同；所有采样与更新应有明确时基。')

# 01
s=new('STM32 外设、信号时序与工程系统设计','ADVANCED COURSE')
shape(s,.70,1.65,7.58,4.68,'panel2')
text(s,'从 GPIO 到片上总线\n从寄存器到实测波形',1.12,2.27,6.75,1.66,30,'white',True)
text(s,'基于 STM32F103C8T6 / 72 MHz 的教学算例',1.18,5.13,6.63,.41,14,'cyan')
shape(s,9.36,2.05,2.75,3.22,'panel','cyan')
text(s,'STM32F103\nCortex-M3\nAHB · APB1 · APB2',9.55,2.82,2.38,1.20,17,'cyan',True,True)
for j in range(7):
 yy=2.27+j*.43;seg(s,9.00,yy,9.34,yy,'orange',2);seg(s,12.14,yy,12.47,yy,'orange',2)
note(s,'课程目标：把“会调用 HAL”升级成“能推导参数、解释时序、验证边界和排查故障”。')

process('学习路径：需求、架构、驱动、时序、验证','OVERVIEW',
[('需求','技术指标'),('架构','资源/时钟'),('驱动','GPIO/TIM/DMA'),('通信','UART/SPI/I²C'),('控制','PID/状态机'),('测试','测量/验收')],
'输出：时钟预算 + 外设分配 + 接口规范 + 波形证据 + 异常记录')
process('系统案例：上位机驱动的电机测速闭环','CASE STUDY',
[('PC','串口调参'),('STM32','控制与采样'),('PWM','驱动器输入'),('H Bridge','功率输出'),('Motor','负载'),('Encoder','反馈采集')],
'控制链：控制周期 1 ms / PWM 20 kHz / USART 115200 / 编码器反馈')
matrix('建立量化指标：需求必须可验证','SPECIFICATION',
['对象','典型目标','关键约束','测试方式'],
[['PWM','20 kHz','PSC / ARR / CCR','示波器'],['采样','2 kHz','源阻抗、ADC 时钟、DMA','采样记录'],['控制','1 ms','最坏执行时间、抖动','GPIO 打点'],['通信','115200 8N1','吞吐、CRC、丢包率','抓包/压力'],['安全','过流切断','硬件路径、失效模式','故障注入']],
'这里的数值是讲解案例，投产应依据器件、负载和任务书重做预算。')
process('芯片内部架构：CPU、总线与外设分区','HARDWARE',
[('CPU','Cortex-M3 / NVIC'),('AHB','存储器总线'),('APB2','GPIO / ADC / TIM1'),('APB1','TIM2 / USART2'),('DMA','外设↔SRAM')],
'总线频率与定时器时钟不同：APB 分频后的某些 TIM 时钟存在倍频规则。')
process('时钟树：8 MHz HSE 如何变成 72 MHz','RCC CLOCK TREE',
[('HSE','8 MHz'),('PLL ×9','72 MHz'),('SYSCLK','72 MHz'),('AHB /1','HCLK 72 MHz'),('APB1 /2','PCLK1 36 MHz'),('TIM2 ×2','72 MHz')],
'ADC 时钟上限、Flash 等待周期、PLL 配置必须独立核查。')
process('复位与启动：为什么代码没有运行到 main()','BOOT & STARTUP',
[('PWR','POR/PDR'),('BOOT','启动模式'),('VECTOR','栈指针/复位向量'),('INIT','时钟/数据段'),('main()','驱动初始化'),('RUN','任务调度')],
'排故顺序：VDD → NRST → BOOT0 → HSE → SWD → 启动文件。')
process('GPIO 内部电路与外部负载的关系','GPIO',
[('GPIO_REG','ODR/BSRR/IDR'),('MODE','输入/复用'),('DRIVER','推挽/开漏'),('PAD','PAx / PBx'),('BOARD','上拉/负载/ESD')],
'开漏高电平来自上拉；不能使用 MCU GPIO 直接驱动大功率负载。')
timing('外部中断：机械按键抖动与软件去抖','EXTI',
[('RAW','11101010000000001111','orange'),('EDGE','00010101000000000000','red'),('FILTER','11111100000000001111','cyan')],
'一个物理按压可能在几毫秒内产生多个有效边沿。',
'不要在中断里忙等；记录时间戳，状态机判稳后再产生按键事件。')
matrix('定时器计算：TIM CLK、PSC、ARR、CCR','TIMER',
['变量','示例取值','作用','公式'],
[['TIM2CLK','72 MHz','定时器输入时钟','PCLK1 ×2'],['PSC','71','预分频后 = 1 MHz','/(PSC+1)'],['ARR','49','每 50 个计数更新','/(ARR+1)'],['CCR','15','PWM 高电平约 15 μs','CCR/(ARR+1)']],
'f_PWM = 72 MHz / [(71+1)×(49+1)] = 20 kHz，周期 = 50 μs。')
timing('PWM：用高电平时间调节平均功率','PWM',
[('CNT','11111111000000001111111100000000','blue'),
 ('PWM30','11100000001110000000111000000000','cyan'),
 ('PWM70','11111110001111111000111111100000','orange')],
'20 kHz 对应每周期 50 μs；改变 CCR 会改变占空比。',
'真实电机电流由电机电感、反电动势与 PWM 频率共同决定。')
process('PWM 预装载：避免周期中途更新带来的毛刺','TIM PRELOAD',
[('控制任务','计算占空比'),('CCR_PRE','写入预装载'),('UEV','更新事件'),('CCR_ACTIVE','周期边界更新'),('PWM_OUT','输出无毛刺')],
'在更改 ARR/CCR、启用同步更新前明确 OCxPE/ARPE 与 UEV 生效时刻。')
timing('半桥互补 PWM：死区与硬件保护','ADVANCED TIMER',
[('CH1','11111100000011111100000011111100','cyan'),
 ('DEAD','00000011110000000011110000000011','red'),
 ('CH1N','00000000111100000000111100000000','orange')],
'死区时间避免上下功率管同时导通；破坏死区会造成直通。',
'TIM1 有高级控制功能；具体通道、死区、Break 行为应查对应参考手册。')
process('ADC + DMA：采样流水线与缓冲区','ADC / DMA',
[('Analog','滤波/限幅'),('S&H','采样保持'),('ADC','12 bit 转换'),('DMA','搬运数据'),('RAM','半缓冲/全缓冲'),('DSP','均值/RMS/保护')],
'DMA 缓冲必须设计读写所有权，避免算法处理时被采样覆盖。')
matrix('ADC 精度预算：12 bit 不等于 12 bit 准确度','ANALOG',
['来源','量化示例','影响','应对'],
[['LSB','3.3 V/4096≈0.806 mV','理想分辨率','校准参考'],['VREF','参考源漂移','满量程误差','测量/稳压'],['ADC IN','采样电容充电','采样误差','源阻抗预算'],['Noise','电源纹波/EMI','有效位数下降','布局/滤波']],
'需要区分分辨率、绝对准确度、ENOB、噪声与 INL/DNL。')
timing('USART：8N1 一帧为什么需要 10 bit','UART',
[('TX','1010011011','cyan'),('START','0100000000','orange'),('STOP','0000000001','green')],
'115200 bit/s → 每 bit 约 8.68 μs；8N1 每字节至少 10 bit。',
'理论载荷吞吐上限约 11 520 byte/s，不含协议头、重传等开销。')
timing('SPI 模式 0：SCK / MOSI / MISO 对齐','SPI',
[('SCK','01010101010101010101010101010101','cyan'),
 ('MOSI','11110000111111110000111100001111','orange'),
 ('MISO','00001111111100001111000011110000','green')],
'CPOL=0、CPHA=0：在规定时钟边沿采样，另一个边沿改变数据。',
'数据在全双工模式下同步移入/移出；还要检查 CS、建立/保持时间。')
timing('I²C 总线：START、ACK 和开漏上拉','I2C',
[('SCL','11100110011001100110011001111111','cyan'),
 ('SDA','11100001110001111000111000111111','orange'),
 ('ACK','11111111111111110000111111111111','green')],
'START：SCL 高时 SDA 由高变低；接收方在第 9 位应答。',
'上升时间受上拉阻值与总线电容影响；具体波形需按手册测量。')
matrix('CPU 搬运 VS DMA：性能差异从哪里来','PERFORMANCE',
['方案','搬运主体','CPU 中断次数','复杂性'],
[['逐字节 ISR','CPU','与数据字节数相关','逻辑简单、负荷大'],
 ['DMA 环形','DMA 控制器','半/满/空闲事件','管理读写指针'],
 ['DMA 双缓冲','DMA+应用任务','块级响应','缓冲区所有权'],
 ['选择依据','吞吐 / 延迟','最坏响应时间','容错需求']],
'DMA 能省 CPU，但并非零总线负荷，更不保证消除缓存覆盖问题。')
timing('NVIC：抢占和临界区导致的时延','INTERRUPTS',
[('MAIN','11111100001111100001111111111111','blue'),
 ('UART','00000011110000001110000000000000','orange'),
 ('TIM','00000000000000000001100000000000','red')],
'高优先级中断可抢占低优先级执行（示例信号）。',
'中断要短；需统计最坏抢占延迟与屏蔽时间，不能只看平均 CPU 占用。')
process('嵌入式软件分层：从裸机到可维护交付','SOFTWARE',
[('APP','状态机/控制'),('SERVICE','日志/队列/调度'),('DRIVER','TIM/ADC/USART'),('BSP','引脚/时钟映射'),('HAL/LL','MCU 抽象')],
'上层业务不应直接操作底层寄存器；硬件更版时集中维护 BSP。')
process('裸机 superloop：控制任务为何不能阻塞','SOFTWARE',
[('TICK','1 ms flag'),('LOOP','周期检查'),('CTRL','控制算法'),('COMM','协议解析'),('WDT','喂狗监控')],
'使用非阻塞函数；不在关键路径执行长时间 HAL_Delay()。')
process('电机控制状态机：正常路径与异常路径','SAFETY',
[('INIT','硬件自检'),('IDLE','PWM 关闭'),('READY','条件检查'),('RUN','闭环运行'),('FAULT','切断功率'),('RECOVER','故障人工复位')],
'FAULT 状态必须定义禁止动作、状态保持及清除条件。')
feedback()
timing('实时调度：1 ms 控制周期的 WCET 预算','REALTIME',
[('ADC','11100000000000000000000000000000','cyan'),
 ('CTRL','00011111100000000000000000000000','orange'),
 ('COMM','00000000111000000000000000000000','green'),
 ('IDLE','00000000000111111111111111111111','blue')],
'样例展示各任务执行段；真实系统应记录最大延迟、抖动与尾部统计。',
'调度是否达标必须覆盖最坏通信输入、故障路径与高负载。')
process('应用协议：序列号、长度、CRC 与帧状态机','COMMUNICATION',
[('SOF','固定同步字'),('LEN','限制最大长度'),('SEQ','丢帧检测'),('CMD','命令/状态'),('DATA','有效载荷'),('CRC16','错误检测')],
'接收实现 WAIT_SOF→HEADER→PAYLOAD→CRC→DISPATCH；CRC 并不等于安全认证。')
process('PCB 工程：电源完整性与信号回流路径','EMC / PCB',
[('DC IN','保护/滤波'),('BUCK','瞬态/纹波'),('3V3','去耦电容'),('MCU','短回流'),('DRIVER','隔离噪声')],
'高 di/dt 电流环路尽可能短；定时采样须避开功率噪声高峰。')
branching('故障树：USART 偶发 CRC 错误','DEBUGGING','串口数据损坏',
[('电气层','电平/共地/干扰'),('时钟层','波特率误差'),('中断层','响应超时'),('缓存层','DMA 覆盖'),('协议层','粘包/CRC')],
'排查证据链：波形→抓包→缓冲指针→错误计数→压力复现。')
matrix('Code Review：工业项目至少审哪些项','DELIVERY',
['对象','必须检查','典型隐患','审查方法'],
[['中断','短 ISR / 优先级','抢占和抖动','Trace'],
 ['缓冲','生命周期/原子性','覆盖/越界','边界测试'],
 ['控制','限幅/失效保护','积分饱和','故障注入'],
 ['接口','CRC/超时/重试','错误恢复失败','模糊测试'],
 ['参数','单位/量程/默认值','量纲错误','参数表']],
'交付不只是源码：应保留电路图、接口说明、量化指标及测试报告。')
matrix('集成验证矩阵：测试必须覆盖失效路径','VALIDATION',
['测试对象','输入刺激','验收条件','证据'],
[['Clock/Reset','反复上电/欠压','可重复启动','NRST / SWD'],
 ['PWM','扫占空比/更新边界','无异常脉宽','示波器'],
 ['ADC/DMA','突变/持续采样','无缓冲数据错位','日志/波形'],
 ['UART','粘包/断链/CRC 错','正确恢复','抓包记录'],
 ['Safety','过流/断传感器','及时关断','故障注入']],
'需由项目批准量化阈值，所有 test case 保留版本、波形与原始数据。')
matrix('算例复盘：20 kHz PWM + 1 ms 控制周期','CALCULATION',
['步骤','设定','推导','最终结果'],
[['时钟','8 MHz×9','PLL','72 MHz'],
 ['APB1','HCLK /2','TIM×2','72 MHz TIM2'],
 ['PWM','PSC 71 / ARR 49','72M/(72×50)','20 kHz'],
 ['占空比','CCR 15','15/50','30%'],
 ['UART','115200 8N1','115200/10','11.52 kB/s']],
'不要把 20 kHz PWM 输出更新与每 1 ms 的速度闭环控制周期混淆。')
process('课程验收：能推导、能测量、能定位、能交付','FINAL REVIEW',
[('理论','解释寄存器'),('设计','资源和指标'),('实现','驱动/状态机'),('测量','时序证据'),('排故','故障树'),('交付','版本和验收')],
'综合作业：完成 PWM+ADC+UART 电机测控系统的框图、参数表和测试记录。')
target=Path('output/STM32_Engineering_Diagram_Enhanced_v4.pptx')
target.parent.mkdir(parents=True,exist_ok=True);r.save(str(target))
print('Created',target,'slides=',len(r.slides),'shapes=',sum(len(s.shapes) for s in r.slides))
