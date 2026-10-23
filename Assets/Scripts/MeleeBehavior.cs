using UnityEngine;

public class MeleeBehavior : MonoBehaviour, IWeaponBehavior
{
    public StatType BehaviorType
    {
        get { return StatType.Melee; }
    }

    private MeleeData meleeData;

    public void Init(WeaponComponentData data)
    {
        meleeData = data as MeleeData;
    }

    public void Execute(int action)
    {
        Debug.Log("Vung kiếm chém cận chiến tầm: " + meleeData.slashRange);
    }
}
