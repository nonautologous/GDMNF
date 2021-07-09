using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using LSL;
using UnityEditor;
//using UnityEditor.Scripting.Python;
public class SendMarkerD : MonoBehaviour
{
    /////////////////////////////////////////////////////////////////////////////////////
    /// Goal of the code: Shuffle a list of 1's and 0's and then present the stimulus////
    /// Presents a red square (0), blue square (1), and cross (null)                 ////
    /// Once presented send the stimulus via the outlet                              ////
    /// Needs to only go for 40 iterations, with 4 seconds of stimulus               ////
    /// followed by 1 second of cross presentation per each iteration                ////
    /////////////////////////////////////////////////////////////////////////////////////
    private liblsl.StreamOutlet outlet;
    private float[] currentSample;

    public string StreamName = "MarkerStream";
    public string StreamType = "stim";
    public string StreamId = "MyStreamID-Unity1234";
    public float itterate = 0;

    // Start is called before the first frame update
    void Start()
    {
        // Change to Channels needed
        liblsl.StreamInfo streamInfo = new liblsl.StreamInfo(StreamName, StreamType, 1, Time.fixedDeltaTime * 1000, liblsl.channel_format_t.cf_float32);
        liblsl.XMLElement chans = streamInfo.desc().append_child("channels");
        chans.append_child("channel").append_child_value("label", "EpochMarker");
        outlet = new liblsl.StreamOutlet(streamInfo);
        currentSample = new float[1];
    }
    // Game objects the fields refer to 
    [SerializeField]
    GameObject Stim1;
    [SerializeField]
    GameObject Stim2;
    [SerializeField]
    GameObject Cross;
    [SerializeField]
    GameObject Check;

    List<int> list = Shuffle();

    public List<int> index = new List<int> { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 };

    public void Initialize()
    {
        // Set the canvas to be only the fixation cross
        Stim1.gameObject.SetActive(false);
        Stim2.gameObject.SetActive(false);
        Cross.gameObject.SetActive(true);
        Check.gameObject.SetActive(true);
        // PythonRunner.RunFile($"{Application.dataPath}/Python/Calibrationcall.py");
        StartCoroutine(Startit());
    }

    public IEnumerator Startit()
    {

        yield return Attempt2(list);
    }

    public IEnumerator Attempt2(List<int> list)
    {
        foreach (int stim in list)
        {
            if (stim == 0)
            {
                Cross.gameObject.SetActive(false);
                Stim1.gameObject.SetActive(true);
                print("stim1" + Time.time);
                currentSample[0] = 1.0f;
                outlet.push_sample(currentSample);
                Cross.gameObject.SetActive(false);
                Stim1.gameObject.SetActive(true);
                yield return new WaitForSecondsRealtime(4.0f);
            }
            if (stim == 1)
            {
                Cross.gameObject.SetActive(false);
                Stim2.gameObject.SetActive(true);
                print("stim2" + Time.time);
                currentSample[0] = 2.0f;
                Cross.gameObject.SetActive(false);
                Stim2.gameObject.SetActive(true);
                outlet.push_sample(currentSample);

                yield return new WaitForSecondsRealtime(4.0f);
            }
            Cross.gameObject.SetActive(true);
            Stim1.gameObject.SetActive(false);
            Stim2.gameObject.SetActive(false);
            print("cross" + Time.time);
            currentSample[0] = 0.0f;
            outlet.push_sample(currentSample);
            Cross.gameObject.SetActive(true);
            Stim1.gameObject.SetActive(false);
            Stim2.gameObject.SetActive(false);
            yield return new WaitForSecondsRealtime(2.0f);
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