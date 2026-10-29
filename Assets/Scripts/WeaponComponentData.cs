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

    public EffectConfig hitEffect;
}

[System.Serializable]
public class MeleeData : WeaponComponentData
{
    public float slashRange;
    public float attackSpeed;

    public EffectConfig hitEffect;
}

[System.Serializable]
public class SniperGunData : WeaponComponentData
{
    public float headshotMultiplier;
    public float damage = 50;
    public float zoomLevel;
    public float bulletSpeedOnSec;
    public Image ScopeUI;

    public EffectConfig hitEffect;
}
