using System.Collections.Generic;
using UnityEngine;

public  class EffectBase
{
    public float duration;
    public bool isTimeOut;
    public Category_Stats statCategory;
    public EffectConfig effectConfig;

    public PlayerComponent who;
    public float rawStat;
    public EffectBase(EffectConfig config, PlayerComponent who)
    {
        effectConfig = config;
        duration = config.duration;
        statCategory = config.statCategory;
        isTimeOut = false;
        this.who = who;

    }

    public void Timer(float deltaTime)
    {
        duration -= deltaTime;
    }
    public void CheckExpired()
    {
        if (duration <= 0)
        {
            isTimeOut = true;
        }
    }
    public void OnApply()
    {
        var stat = who.GetStatOfPlayerByCategory(statCategory);
        if (stat == null) return; 
        rawStat = stat.totalPercentValue;
        stat.totalPercentValue += (effectConfig.perc_Value / 100f);
    }
    public void SetDefaultValueBeforeDeleteEffect()
    {
        who.GetStatOfPlayerByCategory(statCategory).totalPercentValue = rawStat;
    }

}
