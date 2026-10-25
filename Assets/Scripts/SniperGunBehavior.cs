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
    private float damage = 1;
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
        this.damage = sniperData.damage;
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
            if (hitInfo.collider != null)
            {
                Debug.Log("got(name/distance/point)" + hitInfo.collider.name + " / " + hitInfo.distance + " / " + hitInfo.point);
                IDamageable targetHealth = hitInfo.collider.GetComponentInParent<IDamageable>();
                IKnockBack targetKnockback = hitInfo.collider.GetComponentInParent<IKnockBack>();
                if(targetHealth != null) targetHealth.TakeDamage(damage);
                if (targetKnockback != null)
                {
                    Vector3 knockDir = ray.direction;
                    knockDir.y = 0.1f; // Lift it a bit to avoid sinking into the ground
                    knockDir.Normalize();
                    targetKnockback.ExecuteKnockBack(knockDir,90f);
                }    
            }
            
        }
        else Debug.Log("Catch Nothing!!");
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
