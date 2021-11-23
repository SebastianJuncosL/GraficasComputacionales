using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEditor;
using UnityEngine.Networking;


public class Floor_size : MonoBehaviour
{
    [SerializeField] GameObject floorPrefab;
    GameObject floor;
    [SerializeField] int floorHeight;
    [SerializeField] int floorWidth;



    // Start is called before the first frame update
    void Start()
    {
        floor = Instantiate(floorPrefab, Vector3.zero, Quaternion.identity);
        Vector3 floorScale = new Vector3(floorWidth, floorHeight, 1f);
        floor.transform.localScale = floorScale;
        // inicializa la posicion
        floor.transform.position = new Vector3(floorWidth / 2, 0, floorHeight/2);

        floor.transform.eulerAngles = new Vector3(floor.transform.eulerAngles.x + 90, floor.transform.eulerAngles.y, floor.transform.eulerAngles.z);

    }

    // Update is called once per frame
    void Update()
    {

    }
}
