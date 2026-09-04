import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req: Request) => {
  try {
    const { level, coins, stars, score, save_data } = await req.json();
    const supabaseClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      { global: { headers: { Authorization: req.headers.get("Authorization") ?? "" } } }
    );
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401, headers: { "Content-Type": "application/json" } });
    }
    const { data: progress, error: progressError } = await supabaseClient
      .from("player_progress").upsert({
        user_id: user.id, game_id: "desert_rush", current_level: level,
        total_coins: coins, total_stars: stars, total_score: score,
        updated_at: new Date().toISOString(),
      }).select().single();
    if (progressError) throw progressError;
    if (save_data) {
      await supabaseClient.from("cloud_saves").insert({ user_id: user.id, save_data: save_data, slot: 0 });
    }
    return new Response(JSON.stringify({ success: true, progress }), { status: 200, headers: { "Content-Type": "application/json" } });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: { "Content-Type": "application/json" } });
  }
});
