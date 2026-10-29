using Photon.Pun;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerComponent : MonoBehaviourPun,IDamageable,IGetEffect
{
    public RoleConfig roleConfig;

    public Dictionary<Category_Stats,BaseStats_Runtime>dictStats = new Dictionary<Category_Stats,BaseStats_Runtime>();
    public LookingUpDataBase lookingUpData;//move this to agency System Later
    public ReceiveEffect receiveEffect = new ReceiveEffect();
    void Start()
    {
        InitBaseStatForPlayer();
    }
    private void Update()
    {
        receiveEffect.ExecuteEffects();
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
    public BaseStats_Runtime GetStatOfPlayerByCategory(Category_Stats category)
    {
        bool isExist =  dictStats.TryGetValue(category, out BaseStats_Runtime stat);
        if (!isExist)
        {
            Debug.LogWarning("Does not exist stat: " + category + " on: " + gameObject.name);
            return null;
        }
        return stat;
    }
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

    //----------------ReceiveEff---------------//
    public void ReceiveEffect(EffectConfig effectConfig)
    {
        receiveEffect.AddEffect(effectConfig, this);
    }
    public void ApplyEffect(EffectConfig effectConfig)//interface of ReceiveEffect
    {
        if (effectConfig == null || lookingUpData == null) return;
        int id = lookingUpData.GetID(effectConfig);
        if (photonView != null)
        {   // online way call this
            photonView.RPC(nameof(API_Get_Eff_ByID_ReceiveEffect), photonView.Owner, id);
        }
        else
        {   // offline call this 
            ReceiveEffect(effectConfig);
        }
    }
    [PunRPC]
    public void API_Get_Eff_ByID_ReceiveEffect(int id)//API of ReceiveEff
    {
        if (lookingUpData == null) return;
        EffectConfig effectConfig = lookingUpData.Get(id);
        if (effectConfig == null) return;
        ReceiveEffect(effectConfig);
    }
    //----------------ReceiveEff---------------//

}
