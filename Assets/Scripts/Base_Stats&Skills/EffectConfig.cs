using UnityEngine;

[CreateAssetMenu(fileName = "NewEffect_Cfg", menuName = "Configs/Effect Config")]
public class EffectConfig : ScriptableObject
{
    public string effectName ;
    public float duration;
    public float perc_Value; //temporarily it just aim for percentage value
    //advantage set plus , disadvantage set minus (funny feature: if set more than 100% minus that is will be reserved effect)
    public Category_Stats statCategory;
}
