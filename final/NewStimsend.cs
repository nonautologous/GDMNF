using System.Collections.Generic;
using UnityEngine;
using LSL;

public class NewStimsend : MonoBehaviour
{
    private float NextActionTime = 0;
    public float Period = 4.0f;
    private float timer = 0;
    // private int Iterator = 0;
    // private float Stim = 0;
    public liblsl.StreamOutlet outlet;
    private float[] currentSample;

    public string StreamName = "MarkerStream";
    public string StreamType = "stim";
    public string StreamId = "MyStreamID-Unity1234";
    public int Itterate = 0;
    public bool updat = false;
    public float Stim = 0;
    // Start is called before the first frame update
    void Start()
    {
        liblsl.StreamInfo streamInfo = new liblsl.StreamInfo(StreamName, StreamType, 1, 500, liblsl.channel_format_t.cf_float32);
        liblsl.XMLElement chans = streamInfo.desc().append_child("channels");
        chans.append_child("channel").append_child_value("label", "EpochMarker");
        print(streamInfo);
        
        outlet = new liblsl.StreamOutlet(streamInfo);
        print(outlet);
        currentSample = new float[1];
    }
    [SerializeField]
    GameObject Stim1;
    [SerializeField]
    GameObject Stim2;
    [SerializeField]
    GameObject Cross;
    [SerializeField]
    GameObject Check;
    // Update is called once per frame

    public List<int> index = new List<int> { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 };
    public List<int> list = Shuffle();

    public void Initialize()
    {
        // Set the canvas to be only the fixation cross
        Stim1.gameObject.SetActive(true);
        Stim2.gameObject.SetActive(true);
        Cross.gameObject.SetActive(true);
        Check.gameObject.SetActive(true);
        print(outlet);
        //PythonRunner.RunFile($"{Application.dataPath}/Python/Calibrationcall.py");
        updat = true;
    }
    void Update()
    {
        if (updat == true && Itterate <40)
        {
            timer += Time.deltaTime;
            // if time has passed, checks the active stim from the list
            if (timer > NextActionTime)
            {

                if (NextActionTime == Period)
                {
                    // case 0
                    NextActionTime = 1.0f;
                    Cross.gameObject.SetActive(true);
                    Stim1.gameObject.SetActive(false);
                    Stim2.gameObject.SetActive(false);
                    currentSample[0] = 0.0f;
                    print("cross");
                    timer = 0;
                }
                else
                {
                    Stim = list[Itterate];
                    Itterate += 1;
                    if (Stim == 0)
                    {
                        // case 1
                        NextActionTime = Period;
                        // Cross.GetComponent<Renderer>().material.color = Color.clear;
                        // Stim1.GetComponent<Renderer>().material.color = Color.red;
                        // Stim2.GetComponent<Renderer>().material.color = Color.clear;
                        Cross.gameObject.SetActive(false);
                        Stim1.gameObject.SetActive(false);
                        Stim2.gameObject.SetActive(true);
                        // Stim1.GetComponent<Renderer>();

                        // Stim2.GetComponent<Renderer>();
                        currentSample[0] = 1.0f;
                        print("stim1");
                        timer = 0;
                    }
                    if (Stim == 1)
                    {
                        // case 2
                        NextActionTime = Period;
                        Cross.gameObject.SetActive(false);
                        Stim1.gameObject.SetActive(true);
                        Stim2.gameObject.SetActive(false);
                        currentSample[0] = 2.0f;
                        print("stim2");
                        timer = 0;
                    }
                }
                outlet.push_sample(currentSample);
                print("pushed" + Itterate);
            }
        }
        if (updat == true && Itterate >= 40)
        {
            updat = false;
            Itterate = 0;
            Stim1.gameObject.SetActive(true);
            Stim2.gameObject.SetActive(true);
            Cross.gameObject.SetActive(true);
            Check.gameObject.SetActive(true);
        }
    }
    
    static List<int> Shuffle()
    {
        // create a shuffled list of 20 1's and 20 0's 
        var count = 40;
        var list = new List<int>(count);
        var random = new System.Random();
        list.Add(0);
        for (var i = 1; i < count; i++)
        {
            var swap = random.Next(i - 1);
            list.Add(list[swap]);
            list[swap] = i % 2;
        }
        return list;
    }

}
