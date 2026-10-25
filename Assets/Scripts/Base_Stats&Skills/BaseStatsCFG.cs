using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "NewBaseStats_Cfg", menuName = "Configs/BaseStats Config")]
public class BaseStatsCFG : ScriptableObject
{
    public float baseValue = 100;
    public float bonusValue = 0;
    public float percentValue = 1;
    public float totalPercentValue = 1;

    public Category_Stats category_Stats;
}
