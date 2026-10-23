using UnityEngine;

public static class WeaponFactory
{
    // HÀM SẢN XUẤT VŨ KHÍ: Nhận Prefab 3D + Data -> Bàn giao vũ khí hoàn chỉnh
    public static IWeaponBehavior CreateWeapon(GameObject weaponPrefab, WeaponComponentData data, Transform parentSocket)
    {
        if (data == null)
        {
            Debug.LogError("[WeaponFactory] Data truyền vào bị null!");
            return null;
        }

        GameObject weaponInstance;

        // BƯỚC 1: ĐÚC XÁC (Tạo hình thể 3D gắn vào tay Player)
        if (weaponPrefab != null)
        {
            weaponInstance = Object.Instantiate(weaponPrefab, parentSocket);
            weaponInstance.transform.localPosition = new Vector3(0,0.3f,0);
            weaponInstance.transform.localRotation = Quaternion.Euler(-20f, -260f, 260f);
        }
        else
        {
            // Nếu không có Prefab 3D, tạo tạm 1 GameObject rỗng để chạy code
            weaponInstance = new GameObject("Weapon_" + data.GetType().Name);
            if (parentSocket != null)
            {
                weaponInstance.transform.SetParent(parentSocket);
                weaponInstance.transform.localPosition = Vector3.zero;
            }
        }

        // BƯỚC 2: TRA CỨU DANH BẠ (Hỏi Registry xem Data này ứng với Behavior nào)
        System.Type behaviorType = WeaponRegistry.GetBehaviorType(data.GetType());

        if (behaviorType == null)
        {
            Debug.LogError("[WeaponFactory] Không tìm thấy Behavior nào khớp với: " + data.GetType().Name);
            return null;
        }

        // BƯỚC 3: NẠP NÃO (Gắn Behavior vào GameObject)
        Component comp = weaponInstance.AddComponent(behaviorType);
        IWeaponBehavior behavior = comp as IWeaponBehavior;

        if (behavior != null)
        {
            // BƯỚC 4: NẠP ĐẠN / CHỈ SỐ (Gọi Init truyền Data vào)
            behavior.Init(data);
            Debug.Log("<color=green>[WeaponFactory] Đã đúc thành công vũ khí:</color> " + weaponInstance.name);
            return behavior;
        }

        return null;
    }
}
