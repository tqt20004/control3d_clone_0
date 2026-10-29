public interface IDamageable
{
    void TakeDamage(float damage);
}
public interface IGetEffect
{
    void ApplyEffect(EffectConfig effectConfig);
}
