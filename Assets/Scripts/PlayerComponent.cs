using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerComponent : MonoBehaviour,IDamageable
{
    public RoleConfig roleConfig;

    public Dictionary<Category_Stats,BaseStats_Runtime>dictStats = new Dictionary<Category_Stats,BaseStats_Runtime>();
    //public BaseStats_Runtime healthStat = new BaseStats_Runtime();
    //public BaseStats_Runtime defStat = new BaseStats_Runtime();
    // Start is called before the first frame update
    void Start()
    {
        InitBaseStatForPlayer();
    }
    public void InitBaseStatForPlayer()
    {
        if (roleConfig == null || roleConfig.baseStats == null)
        {
            Debug.LogWarning("Does not exist RoleConfig on: " + gameObject.name);
            return;
        }
        dictStats.Clear();
        foreach (var data in roleConfig.baseStats)
        {
            BaseStats_Runtime runtimeStat = new BaseStats_Runtime();
            runtimeStat.InitData(data);

            if (dictStats.ContainsKey(data.category_Stats)) continue;
            dictStats.Add(data.category_Stats, runtimeStat);
        }
    }
    //public void Damage(float damage = 1)
    //{
    //    if(healthStat == null &&  defStat == null) return;
    //    float def = defStat.GetValue();
    //    damage = damage - def;
    //    if (damage < 0) damage = 0;
    //    healthStat.currentValue -= damage;
    //    Debug.Log("currentHealth & Damage:" + healthStat.currentValue+" - "+ damage);
    //}
    public void TakeDamage(float damage)
    {
        var def = dictStats[Category_Stats.def].GetValue();
        damage = damage - def;
        if (damage < 0) damage = 0;
        dictStats[Category_Stats.hp].currentValue -= damage;
        if (dictStats[Category_Stats.hp].currentValue <= 0)
        {
            dictStats[Category_Stats.hp].currentValue = 0;
            Die();
        }
        Debug.Log("currentHealth & Damage:" + dictStats[Category_Stats.hp].currentValue + " - " + damage);
    }

    private void Die()
    {
        EventBus.OnPlayerDied?.Invoke(1);
    }
}
