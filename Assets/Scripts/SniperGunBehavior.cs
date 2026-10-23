using System;
using UnityEngine;
using UnityEngine.UI;

public class SniperGunBehavior : MonoBehaviour, IWeaponBehavior
{
    public static event Action<bool> OnScopeChanged;
    public Camera Camera;
    private float defaultFOV = 60f; 
    private float ZoomFOV = 20f; 
    private bool isZooming = false;
    private float fireRate = 1f;
    public Image ScopeUI;
    public StatType BehaviorType

    {
        get { return StatType.Sniper; }
    }

    private SniperGunData sniperData;

    public void Init(WeaponComponentData data)
    {
        if(data is SniperGunData)
        {
            sniperData = data as SniperGunData;
            AttachData();
        }
    }
    public void AttachData()
    {
        ZoomFOV = sniperData.zoomLevel;
        fireRate = sniperData.bulletSpeedOnSec;
    }
    public void Execute(int action)
    {
        Debug.Log("call Excute in ISniper");
        if (action == 1) Shoot();
        else if (action == 2) ZoomScoop();
        else return;
    }
    public void ZoomScoop()
    {
        if (!CheckCamNullAndTake()) return;
        if (sniperData == null) return;

        isZooming = !isZooming;

        if (isZooming)
        {
            Camera.fieldOfView = ZoomFOV;
            OnScopeChanged?.Invoke(true);
        }
        if (!isZooming)
        {
            Camera.fieldOfView = defaultFOV;
            OnScopeChanged?.Invoke(false);
        }
    }
    public void Shoot()
    { 
        if(!CheckCamNullAndTake()) return; 

        Ray ray = Camera.ViewportPointToRay(new Vector3(0.5f, 0.5f, 0));
        if(Physics.Raycast(ray, out var hitInfo ,500f))
        {
            if (hitInfo.collider != null) Debug.Log("got(name/distance/point)" + hitInfo.collider.name +" / " +hitInfo.distance + " / " + hitInfo.point);
            else Debug.Log("Catch Nothing!!");
        }
    }
    bool CheckCamNullAndTake()
    {
        if (Camera == null)
        {
            Camera = Camera.main;
        }
        if (Camera != null) return true;
        return false;
    }
}
