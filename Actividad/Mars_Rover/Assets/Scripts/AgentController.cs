using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Agents
{
    public List<Vector3> boxesPositions;
    public List<Vector3> collectorsPositions;
}

public class Position
{
    Vector3 deliveryPos;
}

public class AgentController : MonoBehaviour
{
    string url = "http://localhost:8585";
    string initEp = "/init";
    string configEp = "/config";
    string updateEp = "/update";
    [SerializeField] int numRovers;
    [SerializeField] int numBoxes;
    int numPlatform = 1;
    [SerializeField] GameObject roverPrefab;
    [SerializeField] GameObject boxPrefab;
    [SerializeField] GameObject platformPrefab;
    [SerializeField] float updateDelay;

    [SerializeField] GameObject floorPrefab;
    GameObject floor;
    [SerializeField] int floorHeight;
    [SerializeField] int floorWidth;


    

    GameObject[] rover;
    GameObject[] box;
    GameObject platform;
    Agents agents;
    Position delPos;
    float updateTime = 0;


    // Start is called before the first frame update
    void Start()
    {
        startFloor();

        rover = new GameObject[numRovers];
        for (int i = 0; i < numRovers; i++)
        {
            rover[i] = Instantiate(roverPrefab, Vector3.zero, Quaternion.identity);
        }

        box = new GameObject[numBoxes];
        for (int i = 0; i < numBoxes; i++)
        {
            box[i] = Instantiate(boxPrefab, Vector3.zero, Quaternion.identity);
        }


        StartCoroutine(sendConfiguration());
        StartCoroutine()
    }

    // Update is called once per frame
    void Update()
    {
        if (updateTime > updateDelay)
        {
            StartCoroutine(UpdatePositions());
            updateTime = 0;
        }
        updateTime += Time.deltaTime;
    }

    void startFloor()
    {
        floor = Instantiate(floorPrefab, Vector3.zero, Quaternion.identity);
        Vector3 floorScale = new Vector3(floorWidth, floorHeight, 1f);
        floor.transform.localScale = floorScale;
        // inicializa la posicion
        floor.transform.position = new Vector3(floorWidth / 2+0.5f, 0, floorHeight/2+0.5f);

        floor.transform.eulerAngles = new Vector3(floor.transform.eulerAngles.x + 90, floor.transform.eulerAngles.y, floor.transform.eulerAngles.z);
    }

    IEnumerator sendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numRovers", numRovers.ToString());

        UnityWebRequest www = UnityWebRequest.Post(url + configEp, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
        }
        else
        {
            Debug.Log(www.error);
        }
    }

    IEnumerator setDelivery()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + "/getDelivery");
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error)
        else
            delPos = JsonUtility.FromJson<Position>(www.downloadHandler.text);
            platform = Instantiate(platformPrefab, delPos.deliveryPos , Quaternion.identity);
        
    }

    IEnumerator UpdatePositions()
    {
        WWWForm form = new WWWForm();
        form.AddField("numRovers", numRovers.ToString());

        UnityWebRequest www = UnityWebRequest.Get(url + updateEp);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            // Extract the response into an instance of an object
            agents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
            MoveAgents();
        }
        else
        {
            Debug.Log(www.error);
        }
    }

    // Agregar move agents.
}
