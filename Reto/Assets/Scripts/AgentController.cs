// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021 

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;


public class CarData
{
    public int uniqueID;
    public Vector3 position;

}


public class AgentData
{
    public List<Vector3> vehiclesPositions;
}

public class LightStates
{
    public List<string> stoplightsStates;
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://boids.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/updatePositions";
    string getStates = "/updateStates";
    string sendConfigEndpoint = "/";
    string updateEndpoint = "/updateModel";
    string createVehicle = "/generateVehicle";

    AgentData carsData, obstacleData;
    LightStates lightStates;
    GameObject[] agents;
    public List<GameObject> stoplights;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    // Pause the simulation while we get the update from the server
    bool hold = false;

    public GameObject carPrefab;
    public int NAgents;
    public float timeToUpdate = 5.0f, timer, dt;


    void Start()
    {
        carsData = new AgentData();
        lightStates = new LightStates();
        obstacleData = new AgentData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();


        agents = new GameObject[NAgents];



        timer = timeToUpdate;

        for (int i = 0; i < NAgents; i++)
            agents[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);

        StartCoroutine(SendConfiguration());
    }

    private void Update()
    {
        float t = timer / timeToUpdate;
        // Smooth out the transition at start and end
        dt = t * t * (3f - 2f * t);

        if (timer >= timeToUpdate)
        {
            timer = 0;
            hold = true;
            StartCoroutine(UpdateSimulation());
            StartCoroutine(UpdateLights());
        }

        if (!hold)
        {
            if (oldPositions.Count > 0)
            {
                for (int s = 0; s < agents.Length; s++)
                {
                    Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                    agents[s].transform.localPosition = interpolated;

                    Vector3 dir = oldPositions[s] - newPositions[s];
                    agents[s].transform.rotation = Quaternion.LookRotation(dir);

                }
            }
            // Move time from the last frame
            timer += Time.deltaTime;
        }

    }

    IEnumerator UpdateLights()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getStates);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            lightStates = JsonUtility.FromJson<LightStates>(www.downloadHandler.text);

            for (int i = 0; i < stoplights.Count; i++)
            {
                stoplights[i].GetComponent<StopLight>().cambiar_color(lightStates.stoplightsStates[i]);
            }
        }
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            StartCoroutine(GetCarsData());
        }
    }

    IEnumerator SendConfiguration()
    {
        // WWWForm form = new WWWForm();

        // form.AddField("NAgents", NAgents.ToString());

        UnityWebRequest www = UnityWebRequest.Get(serverUrl + sendConfigEndpoint);
        //www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            //StartCoroutine(GetObstacleData());
        }
    }

    IEnumerator GetCarsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            Debug.Log(www.downloadHandler.text);
            carsData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);
            Debug.Log(oldPositions.Count);
            Debug.Log(newPositions.Count);
            newPositions.Clear();

            foreach (Vector3 v in carsData.vehiclesPositions)
                newPositions.Add(v);

            hold = false;
        }
    }

    //     IEnumerator GetObstacleData()
    //     {
    //         UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
    //         yield return www.SendWebRequest();

    //         if (www.result != UnityWebRequest.Result.Success)
    //             Debug.Log(www.error);
    //         else
    //         {
    //             obstacleData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

    //             Debug.Log(obstacleData.positions);

    //             foreach (Vector3 position in obstacleData.positions)
    //             {
    //                 Instantiate(obstaclePrefab, position, Quaternion.identity);
    //             }
    //         }
    //     }
}
