using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using LSL;

public class LSLinput_Change_Animation : MonoBehaviour
{
    public string StreamType = "Parm";
    public float scaleInput = 1.0f;
    liblsl.StreamInfo[] streamInfos;
    liblsl.StreamInlet streamInlet;
    public float[] sample;
    public float[] lastsample;
    private int channelCount = 0;
    public Animation anim;

    private void Start()
    {
        lastsample = new float[1];
        StartCoroutine(Updateproc(1.0f));
    }
    IEnumerator Updateproc(float waitTime)
    {
        print(1);
        while (true)
        {
            if (streamInlet == null)
            {
                streamInfos = liblsl.resolve_stream("type", StreamType, 1, 0.0);
                if (streamInfos.Length > 0)
                {
                    streamInlet = new liblsl.StreamInlet(streamInfos[0]);
                    channelCount = streamInlet.info().channel_count();
                    streamInlet.open_stream();
                    //System.Console.WriteLine(1);
                }
            }
            if (streamInlet != null)
            {
                sample = new float[2];
                if (lastsample == null)
                {
                    lastsample = new float[1];
                }
                double lastTimeStamp = streamInlet.pull_sample(sample, 0.0f);
                //streamInlet.pull_sample(sample);
                //System.Console.WriteLine(2);
                if (lastTimeStamp != 0.0)
                {

                    Process(sample, lastsample, lastTimeStamp);
                    //while ((lastTimeStamp = streamInlet.pull_sample(sample, 0.0f)) != 0)
                    //{
                    //    Process(sample, lastsample, lastTimeStamp);
                    //}
                }
            }
            yield return new WaitForSecondsRealtime(waitTime);
        }
    }

    void Update()
    {
        //if (streamInlet == null)
        //{
        //    streamInfos = liblsl.resolve_stream("type", StreamType, 1, 0.0);
        //    if (streamInfos.Length > 0)
        //    {
        //        streamInlet = new liblsl.StreamInlet(streamInfos[0]);
        //        channelCount = streamInlet.info().channel_count();
        //        streamInlet.open_stream();
        //        //System.Console.WriteLine(1);
        //    }
        //}
        //if (streamInlet != null)
        //{
        //    sample = new float[2];
        //    lastsample = new float[1];
        //    double lastTimeStamp = streamInlet.pull_sample(sample, 0.0f);
        //    //streamInlet.pull_sample(sample);
        //    //System.Console.WriteLine(2);
        //    if (lastTimeStamp != 0.0)
        //    {

        //        Process(sample, lastsample, lastTimeStamp);
        //        //while ((lastTimeStamp = streamInlet.pull_sample(sample, 0.0f)) != 0)
        //        //{
        //        //    Process(sample, lastsample, lastTimeStamp);
        //        //}
        //    }
        //}
        ////sample = new float[2];
        ////streamInfos = liblsl.resolve_stream("type", StreamType, 1, 0.0);
        ////streamInlet = new liblsl.StreamInlet(streamInfos[]);
        ////streamInlet.pull_sample(sample);
        ////System.Console.WriteLine(sample);
        ////Process(sample, lastsample, lastTimeStamp);

    }
    void Process(float[] newSample, float[] lastsample, double timeStamp)
    {
        //System.Console.WriteLine(newSample);
        print(newSample[0] == lastsample[0]);
        if (newSample[0] != lastsample[0])
        {
            //System.Console.WriteLine(newSample);
            anim = gameObject.GetComponent<Animation>();
            print(anim);
            if (newSample[0] == 1)
            {
                if (lastsample[0] == 2)
                {
                    anim["right"].wrapMode = WrapMode.Once;
                    anim["right"].speed = -scaleInput * newSample[1];
                }
                anim["left"].wrapMode = WrapMode.Once;
                anim["left"].speed = scaleInput * newSample[1];
                anim.Play("left");
            }
            if (newSample[0] == 2)
            {
                if (lastsample[0] == 1)
                {
                    
                    anim["left"].wrapMode = WrapMode.Once;
                    anim["left"].speed = -scaleInput * newSample[1];
                    anim.Play("left");
                }
                anim["right"].wrapMode = WrapMode.Once;
                anim["right"].speed = scaleInput * newSample[1];
                anim.Play("right");
            }
            if (newSample[0] == 0)
            {
                if (lastsample[0] == 2)
                {
                    
                    anim["right"].wrapMode = WrapMode.Once;
                    anim["right"].speed = -scaleInput * newSample[1];
                    anim.Play("right");
                }
                if (lastsample[0] == 1)
                {
                    anim["left"].wrapMode=WrapMode.Once ;
                    anim["left"].speed = -scaleInput * newSample[1];
                    anim.Play("left");
                }
            }
        else
        {
            if (newSample[0] == 1)
            {
                anim["left"].speed = scaleInput * newSample[1];
            }
            if (newSample[0] == 2)
            {
                anim["right"].speed = scaleInput * newSample[1];
            }
        }
        }
        lastsample[0] = newSample[0];
    }
}