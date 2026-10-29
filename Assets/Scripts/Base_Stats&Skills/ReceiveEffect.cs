using System.Collections.Generic;
using UnityEngine;


public class ReceiveEffect 
{
    public List<EffectBase> effects = new List<EffectBase>();

    public void AddEffect(EffectConfig effect,PlayerComponent player)
    {
        if (effect == null) return; // check null
        //if existing effect , just refresh duration. If nah just Create new one
        EffectBase existingEffect = effects.Find(e => e.effectConfig == effect);
        if (existingEffect != null)
        {
            existingEffect.duration = effect.duration;
        }
        else
        {
            EffectBase effectBase = new EffectBase(effect, player);
            effects.Add(effectBase);
            effectBase.OnApply();
            Debug.Log("Add Effect: " + effect.effectName + " to: " + player.gameObject.name);
        }
    }
    //if there're any effect , that will be running by the Loop(ExecuteEffects) in PlayerComponent
    //step 1  :check time to know isExpired
    //step 2 :if not expired continue Running , if expired set default value and remove from list
    public void ExecuteEffects()
    {
        if (effects.Count == 0) return;
        
        for (int i = effects.Count - 1; i >= 0; i--)
        {
            effects[i].Timer(Time.deltaTime);
            effects[i].CheckExpired();
            if (effects[i].isTimeOut)
            {
                effects[i].SetDefaultValueBeforeDeleteEffect();
                effects.RemoveAt(i);
                Debug.Log("Effect expired and removed");
            }
        }
    }

}
