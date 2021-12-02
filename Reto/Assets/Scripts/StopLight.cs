using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;


public class StopLight : MonoBehaviour
{
    public string state;

    Light lt;

    void Start()
    {
        lt = GetComponentInChildren<Light>();
        cambiar_color(state);
    }

    // Darken the light completely over a period of 2 seconds.
    public void cambiar_color(string state)
    {
        if (state == "red")
        {
            lt.color = Color.red;
        }
        else if (state == "yellow")
        {
            lt.color = Color.yellow;
        }
        else if (state == "green")
        {
            lt.color = Color.green;
        }

    }

    // void Update()
    // {
    //     if (Input.GetKeyDown("r"))
    //     {
    //         cambiar_color("red");
    //     }
    //     if (Input.GetKeyDown("t"))
    //     {
    //         cambiar_color("green");
    //     }
    // }


}