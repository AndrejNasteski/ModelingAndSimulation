# x = np.linspace(0, 10*np.pi, 100)
# y = np.sin(x)
#
# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# line1, = ax.plot(x, y, 'b-')
#
# for phase in np.linspace(0, 10*np.pi, 100):
#     line1.set_ydata(np.sin(0.5 * x + phase))
#     fig.canvas.draw()
# ____________________
import numpy as np

r = []
mean = 2
for i in range(100):
    r.append(np.random.exponential(scale=2))

opa = np.round(r)
opa = np.array(opa, dtype=np.int32)
print(r)

print(opa)
