using System;
using System.Collections.Generic;

public static class WeaponRegistry
{
    // Dictionary ánh xạ Type của Data sang Type của Behavior
    private static readonly Dictionary<Type, Type> mappingTable = new Dictionary<Type, Type>()
    {
        { typeof(AttackData), typeof(AttackBehavior) },
        { typeof(MeleeData), typeof(MeleeBehavior) },
        { typeof(SniperGunData), typeof(SniperGunBehavior) }
    };

    public static Type GetBehaviorType(Type dataType)
    {
        if (mappingTable.TryGetValue(dataType, out Type behaviorType))
        {
            return behaviorType;
        }
        return null;
    }
}
