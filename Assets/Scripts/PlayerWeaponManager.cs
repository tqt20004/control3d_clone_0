using UnityEngine;

public class PlayerWeaponManager : MonoBehaviour
{
    [Header("Weapon Setup")]
    public EffectConfig stunEffectCfg;
    public Transform handSocket;        // Kéo xương bàn tay của Player vào đây
    public GameObject weaponPrefab3D;   // Kéo Model 3D súng vào đây (hoặc để trống)

    private IWeaponBehavior currentWeaponBehavior;

    private void Start()
    {
        if (handSocket == null)
        {
            handSocket = this.transform; // Mặc định gắn vào chính Player
        }

        // Tạo mẫu data súng tỉa
        SniperGunData sksData = new SniperGunData();
        sksData.zoomLevel = 20f;
        sksData.bulletSpeedOnSec = 1f;
        sksData.headshotMultiplier = 2f;

        if(stunEffectCfg != null)sksData.hitEffect = stunEffectCfg;

        // 👉 ĐÚNG 1 DÒNG ĂN TIỀN: Nhà máy ơi, tạo vũ khí cho tao!
        currentWeaponBehavior = WeaponFactory.CreateWeapon(weaponPrefab3D, sksData, handSocket);

    }

    private void Update()
    {
        if (currentWeaponBehavior == null) return;

        // Chuột Trái -> Bắn (Action 1)
        if (Input.GetMouseButtonDown(0))
        {
            currentWeaponBehavior.Execute(1);
        }

        // Chuột Phải -> Ngắm (Action 2)
        if (Input.GetMouseButtonDown(1))
        {
            currentWeaponBehavior.Execute(2);
        }
    }
}
