import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster


class RealTimePlotter():
    def __init__(self):
        self.axis = plt.axis([-2500, 2500, -2500, 2500])
        self.x = np.full(360,0)
        self.y = np.full(360,0)
    
    def plot(self, pause=.01, min_dist=80):
        self.scatter = plt.scatter(self.x, self.y, color='blue')
        plt.pause(pause)
        self.scatter.remove()
    
    @property
    def X(self):
        return list(zip(self.x,self.y))

    @property
    def linkage(self): 
        return linkage(self.X, 'ward')

    def dendrogram(self):
        # calculate full dendrogram
        plt.figure(figsize=(25, 10))
        plt.title('Hierarchical Clustering Dendrogram')
        plt.xlabel('sample index')
        plt.ylabel('distance')
        dendrogram(
            self.linkage,
            leaf_rotation=90.,  # rotates the x axis labels
            leaf_font_size=8.,  # font size for the x axis labels
        )
        plt.show()

    def set_x(self, x):
        self.x = np.array(x)
        
    def set_y(self, y):
        self.y = np.array(y)

    def cluster(self,kwargs):
        return fcluster(self.linkage, **kwargs)

    def plot_cluster(self,cluster, pause=.01):
        self.scatter = plt.scatter(self.x, self.y, c=cluster, cmap='prism') 
        plt.pause(pause)
        self.scatter.remove()
    
    def calc_distance(self, x1, x2):
        x1 = np.array(x1)
        x2 = np.array(x2)
        return np.sum((x1-x2)**2)**.5

    def angles(self):
        return np.arctan(self.y/self.x)

    def distances(self):
        return (self.y**2+self.x**2)**.5

    def next_distance_cluster(self,distance=200):
        X = np.array(self.X)
        current_pos = X[-1]
        category = []
        for x in X:
            distance = self.calc_distance(x,current_pos)
            current_pos = x
            print(x, distance)

if __name__ == "__main__":
    import pickle as pkl
    with open('data/recorded_lidar.pkl','rb') as f:
        demo_data = pkl.load(f)
    n_frames = len(demo_data)
    print(n_frames)

    rtp = RealTimePlotter()
    while True:
        import time
        for i, (x,y) in enumerate(demo_data):
            rtp.set_x(x)
            rtp.set_y(y)
            #rtp.plot()
            print(i)
            #kwargs = {"t":400,"depth":4,"criterion":"distance"}
            #cluster = rtp.cluster(kwargs)
            rtp.plot()
            time.sleep(1./60)