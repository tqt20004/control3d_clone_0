using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BaseStats_Runtime 
{
    public float baseValue = 1;
    public float bonusValue = 0;
    public float percentValue = 1;
    public float totalPercentValue = 1;

    public float currentValue;

    public void InitData(BaseStatsCFG baseStatsCFG)
    {
        this.baseValue = baseStatsCFG.baseValue;
        this.bonusValue = baseStatsCFG.bonusValue;
        this.percentValue = baseStatsCFG.percentValue;
        this.totalPercentValue = baseStatsCFG.totalPercentValue;

        currentValue = GetValue();
    }
    public float GetValue()
    {
        return ((baseValue * percentValue) + bonusValue) * totalPercentValue;
    }
}
