#%%
import matplotlib.pyplot as plt
import torch
from sympy.polys.subresultants_qq_zz import final_touches

#%%
# Let's define a XOR dataset

# X will be matrix of N 2-dimensional inputs
X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1],], dtype=torch.float64)
# Y is a matrix of N numners - answers
Y = torch.tensor([[0], [1], [1], [0],], dtype=torch.float64)

plt.scatter(
    X[:, 0], X[:, 1], c=Y[:, 0],
)
plt.xlabel("X[0]")
plt.ylabel("X[1]")
plt.axis("square")
#%%
def sigmoid(x):
    return 1 / (1 + torch.exp(-x))



class SmallNet:
    def __init__(self, in_features: int, num_hidden: int, dtype=torch.float32):
        self.W1 = torch.zeros((num_hidden, in_features), dtype=dtype)
        self.b1 = torch.zeros((num_hidden,), dtype=dtype)
        self.W2 = torch.zeros((1, num_hidden), dtype=dtype)
        self.b2 = torch.zeros((1,), dtype=dtype)
        self.init_params()

    def init_params(self):
        self.W1 = torch.randn_like(self.W1) * 0.5
        self.b1 = torch.randn_like(self.b1) * 0.5
        self.W2 = torch.randn_like(self.W2) * 0.5
        self.b2 = torch.randn_like(self.b2) * 0.5


    def forward(self, X, Y=None, do_backward=False):
        # TODO Problem 1: Fill in details of forward propagation

        # Input to neurons in 1st layer
        A1 = X @ self.W1.T + self.b1
        # Outputs after the sigmoid non-linearity
        O1 = sigmoid(A1)
        # Inputs to neuron in the second layer
        A2 = O1 @ self.W2.T + self.b2
        # Outputs after the sigmoid non-linearity
        O2 = sigmoid(A2)

        # When Y is none, simply return the predictions. Else compute the loss
        if Y is not None:
            loss = -Y * torch.log(O2) - (1 - Y) * torch.log(1 - O2)
            # normalize loss by batch size
            loss = loss.sum() / X.shape[0]
        else:
            loss = torch.nan

        if do_backward:
            # TODO in Problem 2:
            # fill in the gradient computation
            # Please note, that there is a correspondance between
            # the forward and backward pass: with backward computations happening
            # in reverse order.
            # We save the gradients with respect to the parameters as fields of self.
            # It is not very elegant, but simplifies training code later on.

            # A2_grad is the gradient of loss with respect to A2
            # Hint: there is a concise formula for the gradient
            # of logistic sigmoid and cross-entropy loss
            A2_grad = (O2 - Y) / X.shape[0] # need to normalise gradient by batch size
            self.b2_grad = A2_grad.sum(0)
            self.W2_grad = A2_grad.T @ O1
            O1_grad = A2_grad @ self.W2
            A1_grad = O1_grad * O1 * (1 - O1)
            self.b1_grad = A1_grad.sum(0)
            self.W1_grad = A1_grad.T @ X

        return O2, loss
#%%

# TODO Problem 1:
# Set the weight values to solve the XOR problem

net = SmallNet(2, 2, dtype=torch.float64)
net.W1 = torch.tensor([[7.0, 7.0], [-5.0, -5.0]], dtype=torch.float64)
net.b1 = torch.tensor([-2.5, 7.5], dtype=torch.float64)
net.W2 = torch.tensor([[5.0, 5.0]], dtype=torch.float64)
net.b2 = torch.tensor([-7.35], dtype=torch.float64)


# Hint: since we use the logistic sigmoid activation, the weights may need to
# be fairly large


predictions, loss = net.forward(X, Y, do_backward=True)
for x, p in zip(X, predictions):
    print(f"XORnet({x}) = {p[0]}")
#%%
def check_grad(net, param_name, X, Y, eps=1e-5):
    """A gradient checking routine"""

    param = getattr(net, param_name)
    param_flat_accessor = param.reshape(-1)

    grad = torch.empty_like(param)
    grad_flat_accessor = grad.reshape(-1)

    net.forward(X, Y, do_backward=True)
    orig_grad = getattr(net, param_name + "_grad")
    assert param.shape == orig_grad.shape

    for i in range(param_flat_accessor.shape[0]):
        orig_val = param_flat_accessor[i].item()
        param_flat_accessor[i] = orig_val + eps
        _, loss_positive = net.forward(X, Y)
        param_flat_accessor[i] = orig_val - eps
        _, loss_negative = net.forward(X, Y)
        param_flat_accessor[i] = orig_val
        grad_flat_accessor[i] = (loss_positive - loss_negative) / (2 * eps)
    assert torch.allclose(grad, orig_grad)
    return grad, orig_grad

#%%
# Hint: use float64 for checking the correctness of the gradient

for param_name in ["W1", "b1", "W2", "b2"]:
    check_grad(net, param_name, X, Y)
#%%
net = SmallNet(2, 10, dtype=torch.float64)

alpha = 0.01  # set a learning rate

for i in range(100000):
    _, loss = net.forward(X, Y, do_backward=True)
    if (i % 5000) == 0:
        print(f"after {i} steps \tloss={loss}")
    for param_name in ["W1", "b1", "W2", "b2"]:
        param = getattr(net, param_name)
        # Hint: use the construct `param[:]` to change the contents of the array!
        # Doing instead `param = new_val` simply changes to what the variable
        # param points to, without affecting the network!
        # alternatively, you could do setattr(net, param_name, new_value)

        # Retrieve the gradient from backpropagation
        grad = getattr(net, param_name + "_grad")

        param[:] = param - alpha * grad
#%%
predictions, loss = net.forward(X, Y, do_backward=True)
for x, p in zip(X, predictions):
    print(f"XORnet({x}) = {p[0]}")
#%%
# TODO:
# Generate data for a 3D XOR task
# Then estimate the success rate of training the network with diferent
# hidden sizes.

# XOR TASK:
X3 = torch.tensor([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                   [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]],
                  dtype=torch.float64)
# XOR ANSWERS (tue when odd number of inputs are 1):

Y3 = torch.tensor([[0], [1], [1], [0], [1], [0], [0], [1]],
                 dtype=torch.float64)
results = {}
num_runs = 10


for hidden_dim in [2, 3, 5, 10, 20]:
    # TODO: run a few trainings and record the fraction of successful ones
    successful_runs = 0

    for run in range(num_runs):
        net = SmallNet(3, hidden_dim, dtype=torch.float64)
        alpha = 0.01

        for i in range(100000): # iterations per training attempt
            _, loss = net.forward(X3, Y3, do_backward=True)
            if (i % 5000) == 0:
                print(f"after {i} steps \tloss={loss}")
            for param_name in ["W1", "b1", "W2", "b2"]:
                # Gradient descent step
                param = getattr(net, param_name)
                grad = getattr(net, param_name + "_grad")
                param[:] = param - alpha * grad

        predictions, final_loss = net.forward(X3, Y3, do_backward=False)
        correct = ((predictions > 0.5).float() == Y3).all()

        if correct:
            successful_runs += 1

    success_rate = successful_runs / num_runs
    results[hidden_dim] = success_rate
    print(f"Hidden size {hidden_dim}: Success rate = {success_rate:.2f}")

#%%
