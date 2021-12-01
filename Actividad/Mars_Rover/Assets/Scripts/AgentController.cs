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
    public Vector3 deliveryPos;
}

public class AgentController : MonoBehaviour
{
    string url = "http://127.0.0.1:8585";
    string initEp = "/init";
    string positionEp = "/UpdatePositions";
    string modelEp = "/updateModel";
    [SerializeField] int numRovers;
    [SerializeField] int numBoxes;
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
            rover[i].transform.Rotate(-90.0f, 0.0f, 0.0f);
        }

        box = new GameObject[numBoxes];
        for (int i = 0; i < numBoxes; i++)
        {
            box[i] = Instantiate(boxPrefab, Vector3.zero, Quaternion.identity);
        }


        StartCoroutine(sendConfiguration());
        StartCoroutine(setDelivery());
        StartCoroutine(UpdatePositions());
    }

    // Update is called once per frame
    void Update()
    {
        if (updateTime > updateDelay)
        {
            StartCoroutine(UpdateModel());
            StartCoroutine(UpdatePositions());
            MoveAgents();
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
        floor.transform.position = new Vector3(floorWidth / 2-0.5f, 0, floorHeight/2-0.5f);

        floor.transform.eulerAngles = new Vector3(floor.transform.eulerAngles.x + 90, floor.transform.eulerAngles.y, floor.transform.eulerAngles.z);
    }

    IEnumerator sendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numRovers", numRovers.ToString());
        form.AddField("numBoxes", numBoxes.ToString());
        form.AddField("width", floorWidth.ToString());
        form.AddField("height", floorHeight.ToString());

        UnityWebRequest www = UnityWebRequest.Post(url + initEp, form);
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
            Debug.Log(www.error);
        else
            Debug.Log(www.downloadHandler.text);
            delPos = JsonUtility.FromJson<Position>(www.downloadHandler.text);
            platform = Instantiate(platformPrefab, delPos.deliveryPos , Quaternion.identity);
    }

    IEnumerator UpdateModel()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + modelEp);
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

    IEnumerator UpdatePositions()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + positionEp);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(www.downloadHandler.text);
            // Extract the response into an instance of an object
            agents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);
        }
        else
        {
            Debug.Log(www.error);
        }
    }

    void MoveAgents()
    {
        for (int i = 0; i < numRovers; i++)
        {
            rover[i].transform.position = agents.collectorsPositions[i];
        }
        for (int i = 0; i < numBoxes; i++)
        {
            box[i].transform.position = agents.boxesPositions[i];
        }
    }
}
