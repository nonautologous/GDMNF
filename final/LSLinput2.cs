﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using LSL;

public class LSLinput2 : MonoBehaviour
{
    public string StreamType = "EEG";
    public float scaleInput = 0.1f;
    liblsl.StreamInfo[] streamInfos;
    liblsl.StreamInlet streamInlet;
    float[] sample;
    private int channelCount = 0;

    void Update()
    {
        if (streamInlet == null)
        {
            streamInfos = liblsl.resolve_stream("type", StreamType, 1, 0.0);
            if (streamInfos.Length > 0)
            {
                streamInlet = new liblsl.StreamInlet(streamInfos[0]);
                channelCount = streamInlet.info().channel_count();
                streamInlet.open_stream();
            }
        }

        if (streamInlet != null)
        {
            sample = new float[channelCount];
            double lastTimeStamp = streamInlet.pull_sample(sample, 0.0f);
            if (lastTimeStamp != 0.0)
            {
                Processw(sample, lastTimeStamp);
                while ((lastTimeStamp = streamInlet.pull_sample(sample, 0.0f)) != 0)
                {
                    Processw(sample, lastTimeStamp);
                }
            }
        }
    }
    void Processw(float[] newSample, double timeStamp)
    {
        var inputVelocity = new Vector3(scaleInput * (newSample[0] - 0.5f), scaleInput * (newSample[1] - 0.5f), scaleInput * (newSample[2] - 0.5f));
        gameObject.transform.position = gameObject.transform.position + inputVelocity;
    }
}