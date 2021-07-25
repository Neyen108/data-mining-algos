#include <stdio.h>
#include <stdlib.h>
#include <time.h>

struct Point
{
    double x, y; // coordinates
    int cluster;
    double minDist;
} Point;

double distance(struct Point a, struct Point b)
{
    return ((a.x - b.x) * (a.x - b.x)) + ((a.y - b.y) * (a.y - b.y));
}

void calculateNewMeans(struct Point *means, struct Point *points, int numPoints, int k)
{
    int nPoints[k]; //to hold the number of points in each cluster
    double sumX[k]; //to hold the x coordinates sum of the points in each cluster
    double sumY[k]; //to hold the y coordinates sum of the points in each cluster

    // Initialise with zeroes
    for (int i = 0; i < k; i++)
    {
        nPoints[i] = 0;
        sumX[i] = 0.0;
        sumY[i] = 0.0;
    }

    //itereate through the points to get which cluster the point is in
    for (int i = 0; i < numPoints; i++)
    {
        int clusterId = points[i].cluster;
        nPoints[clusterId]++;
        sumX[clusterId] += points[i].x;
        sumY[clusterId] += points[i].y;

        //reset minDist
        points[i].minDist = __DBL_MAX__;
    }

    //Compute the new means
    for (int i = 0; i < k; i++)
    {
        means[i].x = sumX[i] / nPoints[i];
        means[i].y = sumY[i] / nPoints[i];
    }
}

//kmeans clustering algorithm
void kMeansClustering(struct Point *points, int numPoints, int epochs, int k)
{
    //initialize random means
    struct Point *means = malloc(k * sizeof(Point));
    srand(time(0));
    for (int i = 0; i < k; i++)
    {
        means[i] = points[rand() % numPoints];
    }

    while (epochs--)
    {
        //assigning points to a cluster
        for (int i = 0; i < k; i++)
        {
            //current cluster
            int clusterId = i;
            //current mean
            struct Point mean = means[i];

            for (int j = 0; j < numPoints; j++)
            {
                //check distance from the mean, if distance is less then update cluster
                double dist = distance(points[j], mean);
                if (dist < points[j].minDist)
                {
                    points[j].minDist = dist;
                    points[j].cluster = clusterId;
                }
            }
        }

        //find the new means
        calculateNewMeans(means, points, numPoints, k);
    }
}

void writeToFile(struct Point *points, int numPoints, int k)
{
    FILE *fptr;

    if ((fptr = fopen("result.txt", "w")) == NULL)
    {
        printf("Error Opening File.");
        exit(1);
    }

    for (int j = 0; j < k; j++)
    {
        fprintf(fptr, "\n%s : %d\n", "Cluster", j + 1);
        for (int i = 0; i < numPoints; i++)
        {
            if (points[i].cluster == j)
            {
                fprintf(fptr, "(%.2lf,%.2lf)\n", points[i].x, points[i].y);
            }
        }
    }

    fclose(fptr);
}

int main()
{
    struct Point *points = malloc(4000 * sizeof(Point));

    FILE *fptr;

    //reading from file
    if ((fptr = fopen("k-means-data.txt", "r")) == NULL)
    {
        printf("Error Opening File.");
        exit(1);
    }

    //initializing the points from data in the file
    int idx = 0;
    char line[100];
    while (fgets(line, 100, fptr) != NULL)
    {
        sscanf(line, "%lf %lf", &points[idx].x, &points[idx].y);
        points[idx].cluster = -1;          // no default cluster
        points[idx].minDist = __DBL_MAX__; // default infinite dist to nearest cluster
        idx++;
    }
    fclose(fptr);

    //total number of points read from file
    int numPoints = idx;

    //user input for clusters and epochs
    int k, epochs;
    printf("How many clusters do you want : ");
    scanf("%d", &k);
    printf("For how many epochs do you want to run the k-means clustering algorithm: ");
    scanf("%d", &epochs);

    kMeansClustering(points, numPoints, epochs, k);

    writeToFile(points, numPoints, k);
    printf("Results stored in result.txt\n");
}
