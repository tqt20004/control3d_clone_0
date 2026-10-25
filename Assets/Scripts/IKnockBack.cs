using System.Collections;
using System.Collections.Generic;
using UnityEditor.ShaderGraph.Internal;
using UnityEngine;

public interface IKnockBack 
{
    void ExecuteKnockBack(Vector3 dir, float force);
}
