using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class Manager : MonoBehaviour
{
    [SerializeField]
    Transform UIPanel;
    
    [SerializeField]

    Transform CaliPanel;

    [SerializeField]
    Camera Camera;

    [SerializeField]
    Camera fps;
    void Start()
    {
        UIPanel.gameObject.SetActive(true);
        CaliPanel.gameObject.SetActive(false);
        Camera.enabled=false;
        fps.enabled= true;
    }
    void Update()
    {
        if(Input.GetKeyDown(KeyCode.Escape))
        Quit();
    }
    public void Menu()
    {
        UIPanel.gameObject.SetActive(true);
    }
    public void Quit()
    {
        Application.Quit();
    }

    public void Calibration()
    {
        UIPanel.gameObject.SetActive(false);
        CaliPanel.gameObject.SetActive(true);
    }
    public void Live()
    {
        UIPanel.gameObject.SetActive(false);
        CaliPanel.gameObject.SetActive(false);
        Camera.enabled = false;
        fps.enabled = true;
    }

    public void Live_Allocentric()
    {
        UIPanel.gameObject.SetActive(false);
        CaliPanel.gameObject.SetActive(false);
        Camera.enabled = true;
        fps.enabled = false;
    }

}