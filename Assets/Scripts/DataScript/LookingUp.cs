using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "EffectDatabase", menuName = "Configs/Effect Database")]
public class LookingUpDataBase : ScriptableObject
{
    public List<TypeEf> active_effectList = new List<TypeEf>();    
    public EffectConfig Get(int targetID)
    {
        foreach (var i in active_effectList)
        {
            if (i.id == targetID)
            {
                return i.config; 
            }
        }

        Debug.LogError("Cant Look Up: " + targetID);
        return null;
    }
    // Method get ID form EffectCfg:
    public int GetID(EffectConfig config)
    {
        foreach (var pair in active_effectList)
        {
            if (pair.config == config) return pair.id;
        }
        return -1;
    }
}
[System.Serializable]
public struct TypeEf
{
    public int id;
    public EffectConfig config;
}
