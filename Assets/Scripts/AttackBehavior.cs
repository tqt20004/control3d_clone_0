using UnityEngine;

public class AttackBehavior : MonoBehaviour, IWeaponBehavior
{
    public StatType BehaviorType
    {
        get { return StatType.Attack; }
    }

    private AttackData attackData;

    public void Init(WeaponComponentData data)
    {
        attackData = data as AttackData;
    }

    public void Execute(int action)
    {
        Debug.Log("Bắn súng thường: " + attackData.damage);
    }
}
