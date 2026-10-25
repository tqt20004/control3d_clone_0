using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[CreateAssetMenu(fileName = "NewRole_Cfg", menuName = "Configs/Role Config")]
public class RoleConfig : ScriptableObject
{
    public string roleName;
    public List<BaseStatsCFG> baseStats; 
}
public enum Category_Stats
{
    hp,
    def
}
