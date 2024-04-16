import matplotlib.pyplot as plt
import numpy as np

# Generate some data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)

# Create the first figure
plt.figure(1)
plt.plot(x, y1)
plt.title('Sine Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')

# Create the second figure
plt.figure(2)
plt.plot(x, y2)
plt.title('Cosine Wave')
plt.xlabel('x')
plt.ylabel('cos(x)')

# Create the third figure
plt.figure(3)
plt.plot(x, y3)
plt.title('Tangent Wave')
plt.xlabel('x')
plt.ylabel('tan(x)')

# Display all figures
plt.show()
