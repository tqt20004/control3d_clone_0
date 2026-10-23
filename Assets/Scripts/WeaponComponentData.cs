using System;
using UnityEngine.UI;

[System.Serializable]
public abstract class WeaponComponentData
{
    // Lớp cha trừu tượng cho tất cả Data hành vi
}

[System.Serializable]
public class AttackData : WeaponComponentData
{
    public float damage;
    public float fireRate;
}

[System.Serializable]
public class MeleeData : WeaponComponentData
{
    public float slashRange;
    public float attackSpeed;
}

[System.Serializable]
public class SniperGunData : WeaponComponentData
{
    public float headshotMultiplier;
    public float zoomLevel;
    public float bulletSpeedOnSec;
    public Image ScopeUI;
}
