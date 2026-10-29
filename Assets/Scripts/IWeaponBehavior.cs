public interface IWeaponBehavior
{

    StatType BehaviorType { get; }
    void Init(WeaponComponentData data);
    void Execute(int action = 0);
}
